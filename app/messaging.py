def send_message( message, queue ):
    """queue something (via rabbitmq)"""
    # RabbitMQ setup
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
        body          = message,
        properties    = pika.BasicProperties(
            delivery_mode = 2,         )
    )
    connection.close()
    return OK, session
