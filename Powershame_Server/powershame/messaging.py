from powershame import app
import logging
import pika
import json


def send_message( message, queue ):
    """queue something (via rabbitmq)"""
    # RabbitMQ setup
    logging.debug('preparing messge for queue: %s'%str(message) )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters( host=app.config['QUEUE_HOST'] ) )
    channel = connection.channel()
    channel.basic_qos( prefetch_count=1 )
    channel.queue_declare(
        queue = queue, 
        durable = True ) 
    # send message
    channel.basic_publish(
        exchange      = '',
        routing_key   = queue,
        body          = json.dumps(message),
        properties    = pika.BasicProperties( delivery_mode = 2 )
    )
    connection.close()
    logging.debug('sent message %s'%str(message) )
    return True

if __name__=='__main__':
    send_message( {'session_id':61},'rendering' )
