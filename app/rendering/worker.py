import os
import sys
from app import app,db,models
from app.models.session import Session
import pika
import json
import logging
from datetime import datetime
from session_renderer import SessionRenderer

HOST = app.config['QUEUE_HOST']
RENDERING_QUEUE = app.config['RENDERING_QUEUE']
print HOST
print RENDERING_QUEUE

renderer = SessionRenderer( 
    app.config['RENDERER_KEY'], 
    app.config['RENDERER_SECRET'], 
    app.config['PIC_BUCKET'], 
    app.config['VID_BUCKET'], 
    '/tmp' )

def send_notification( message ):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters( host=app.config['QUEUE_HOST'] ) )
    channel = connection.channel()
    channel.basic_qos( prefetch_count=1 )
    channel.queue_declare(
        queue = app.config['NOTIFICATION_QUEUE'], 
        durable = True ) 
    # send message
    channel.basic_publish(
        exchange      = '',
        routing_key   = app.config['NOTIFICATION_QUEUE'],
        body          = message,
        properties    = pika.BasicProperties(
            delivery_mode = 2,         )
    )
    connection.close()

def render_worker(ch, method, properties, body):
    db.session.rollback()
    logging.debug('starting render process')
    logging.debug('got: %s'% body )
    try:
        session = json.loads( body )
        key_path = user_id + '/' + session.name + '.mkv'
        url, expiration = renderer.render( session.id, session.screenshots )
        session.url_expire = expiration
        session.url = url
        db.session.commit()
        send_notification( json.dumps({ 'session_id': session_id }) )
        logging.debug('finished rendering session: %s'%str(session))
        ch.basic_ack(delivery_tag = method.delivery_tag)
        logging.debug('ack tack')
    except Exception as e:
        logging.critical( e )
        ch.basic_reject(delivery_tag = method.delivery_tag)
        return

if __name__ == '__main__':
    root = logging.getLogger()

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    root.setLevel(logging.DEBUG)

    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host = HOST ))
    channel = connection.channel()
    channel.queue_declare(queue=RENDERING_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(render_worker,
                          queue=RENDERING_QUEUE)
    channel.start_consuming()
