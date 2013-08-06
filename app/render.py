from celery import Celery
from config import *
from session_renderer import SessionRenderer

celery = Celery('render', backend='amqp', broker='amqp://guest@localhost//')
renderer=SessionRenderer( ACCESS_ID, SECRET, PIC_BUCKET_NAME, VID_BUCKET_NAME, '/tmp' )

@celery.task
def render( username, session_name):
    return renderer.render(  username, session_name )
