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
    logging.debug('starting render process')
    logging.debug('got: %s'% body )
    try:
        ps_session = json.loads( body )
        for k in ps_session:
            print k,ps_session[k]
        key_path = str(ps_session['user']) + '/' + ps_session['name'] + '.mkv'
        url, expiration = renderer.render( ps_session['id'], ps_session['screenshots'] )
        session_id = ps_session['id']
        update_session_db( session_id, url, expiration )
        send_notification( json.dumps({ 'session_id': session_id }) )
        logging.debug('finished rendering session')
        ch.basic_ack(delivery_tag = method.delivery_tag)
    except Exception as e:
        logging.critical( e )
        ch.basic_reject(delivery_tag = method.delivery_tag)
        return
    finally:
        db.session.commit()

def update_session_db( session_id, url, expiration ):
    db.session.rollback()
    session = Session.query.get( session_id )
    session.url_expire = expiration
    session.url = url
    db.session.commit()

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
