from app import app
from app import db
from app import models
from app.models.session import Session
from app.models.user import User
from app.models.contact_info import ContactInfo
import pika
import json
import boto.ses

import sys
import logging

HOST = app.config['QUEUE_HOST']
RENDERING_QUEUE = app.config['RENDERING_QUEUE']
NOTIFICATION_QUEUE = app.config['NOTIFICATION_QUEUE']

def send_notification_email( session ):
    db.session.rollback()
    logging.debug('starting notification process')
    user = User.query.get( session.user )
    shamers = session.shamers
    url = session.url
    addresses = [ shamer.identifier for shamer in shamers ]
    user_email = user.contact_info.first().identifier
    addresses.append( user_email )
    print addresses
    conn = boto.ses.connect_to_region(
            'us-east-1',
            aws_access_key_id='AKIAIK3XBZAB7VP74FNQ',
            aws_secret_access_key='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')
    print conn.send_email(
        'CaptainShame@powershame.com',
        'Powershame for %s' % user.username,
        url,
        addresses )
    logging.debug('sent email')
    print 'done'

def notification_worker(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    db.session.rollback()
    session_id = json.loads(body)['session_id']
    session = Session.query.filter_by( id=session_id ).first()
    send_notification_email( session )
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)


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
channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(notification_worker,
                      queue=NOTIFICATION_QUEUE)

print 'starting worker'
channel.start_consuming()
