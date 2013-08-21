from app import app
from app.models.session import Session
import pika
import json
import boto.ses

HOST = app.config['QUEUE_HOST']
RENDERING_QUEUE = app.config['RENDERING_QUEUE']
NOTIFICATION_QUEUE = app.config['NOTIFICATION_QUEUE']

def send_notification_email( session, url ):
    user = session.shamee
    print user
    shamers = session.shamers
    addresses = [ shamer.identifier for shamer in shamers ]
    user_email = user.contact_info.first().identifier
    print user_email
    addresses.append( user_email )
    print addresses
    conn = boto.ses.connect_to_region(
            'us-east-1',
            aws_access_key_id='AKIAIK3XBZAB7VP74FNQ',
            aws_secret_access_key='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')
    conn.send_email(
        'CaptainShame@powershame.com',
        'Powershame for %s' % user.username,
        url,
        addresses )
    print 'done'

def notification_worker(ch, method, properties, body):
    print "worker started"
    print " [x] Received %r" % (body,)
    session_id = json.loads(body)['session_id']
    session = Session.query.filter_by( id=session_id ).first()
    print session
    url = json.loads(body)['url']
    print url
    send_notification_email( session, url )
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host = HOST ))
channel = connection.channel()
channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(notification_worker,
                      queue=NOTIFICATION_QUEUE)

print 'starting worker'
channel.start_consuming()
