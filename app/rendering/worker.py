from app import app
from app.models.session import Session
import pika
import json
from session_renderer import SessionRenderer

HOST = app.config['QUEUE_HOST']
RENDERING_QUEUE = app.config['RENDERING_QUEUE']
NOTIFICATION_QUEUE = app.config['NOTIFICATION_QUEUE']


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
    vars = json.loads( body )
    try:
        session_id = int(vars['session_id'])
        session = Session.query.filter_by( id=session_id ).first()
        user_id = session.shamee.id
        session_name = session.name
        key_path = user_id + '/' + session_name + '.mkv'
        video_path = renderer.render(username, session_name)
        url = renderer.upload_video( video_path, key_path )
        #TODO: update db
        send_notification( json.dumps({ 'session_id': session_id, 'url': url }) )
    except KeyError:
        pass
    ch.basic_ack(delivery_tag = method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host = HOST ))
channel = connection.channel()
channel.queue_declare(queue=RENDERING_QUEUE, durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(render_worker,
                      queue=RENDERING_QUEUE)

channel.start_consuming()
