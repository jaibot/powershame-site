import os
import sys
from app import app,db,models
from app.models.session import Session
import pika
import json
import logging
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
    vars = json.loads( body )
    logging.debug('got: %s'%str(vars))
    try:
        session_id = int(vars['session_id'])
        session = Session.query.get( session_id )
        if not session:
            logging.debug('failed on session: %s'%str(session))
            ch.basic_reject(delivery_tag = method.delivery_tag)
            return #FIX LATER - send FAILURE ack
        logging.debug('session: %s'%str(session))
        user_id = str(session.user)
        prefix = '/'.join( (user_id, str(session_id)) ) +'/'
        key_path = user_id + '/' + session.name + '.mkv'
        url = renderer.render( prefix, key_path )
        #TODO: update db
        send_notification( json.dumps({ 'session_id': session_id, 'url': url }) )
    except KeyError:
        print 'ohno'
        return
    except IOError:
        pass
    logging.debug('finished rendering session: %s'%str(session))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    logging.debug('ack tack')

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
