#TODO: Make this entire file redundant and delete, it is needlessly confusing
from flask import request, abort, jsonify, session
from flask.ext.login import LoginManager,login_user

from app import app
from app import db
from app import login_manager

from app.permission_generator import get_temp_upload_creds
from app.models.user import User, get_user_by_login
from app.models.session import Session
from app.models.client import Client
from app.models.upload_creds import UploadCreds

from datetime import datetime,timedelta

import pika
import json

FAIL,OK=0,1

def create_session( user, name ):
    pass #TODO

def get_or_update_upload_creds( user ):
    all_creds = user.upload_creds.all()
    if len(all_creds)==0:
        return new_upload_creds( user )
    elif len(all_creds)>1: #covering the weird case where the user got extra creds
        all_creds.sort( key = lambda x: x.expiration )
        for c in all_creds[:-1]:
            db.session.delete( c )
        db.session.commit()
    creds = all_creds[-1]
    if creds.expired():
        return new_upload_creds( user )
    else:
        return OK, creds

def new_upload_creds( user ):
    old_creds = user.upload_creds.first()
    if old_creds:
        db.session.delete( old_creds )
        db.session.commit()
    lifetime_in_seconds = app.config['UPLOAD_CREDS_LIFETIME']
    creds = get_temp_upload_creds( user.username, lifetime_in_seconds )
    expiration = datetime.now() + timedelta( seconds = lifetime_in_seconds )
    upload_creds = UploadCreds(
            user,
            expiration,
            creds.access_key,
            creds.secret_key,
            creds.session_token )
    return OK, upload_creds

def render_session( session ):
    """queue rendering of a completed powershame session (via rabbitmq)"""
    user = session.owner
    session_name = session.name
    message = json.dumps( 
        { 'username': user.username, 
          'session_name': session_name } ) 
    # RabbitMQ setup
    connection = pika.BlockingConnection(
        pika.ConnectionParameters( host=app.config['QUEUE_HOST'] ) )
    channel = connection.channel()
    channel.basic_qos( prefetch_count=3 )
    channel.queue_declare(
        queue = app.config['RENDERING_QUEUE'], 
        durable = True ) 
    # send message
    channel.basic_publish(
        exchange      = '',
        routing_key   = app.config['RENDERING_QUEUE'],
        body          = message,
        properties    = pika.BasicProperties(
            delivery_mode = 2,         )
    )
    connection.close()
    return OK

def notify_rendered_session( session ):
    shamers = session.shamers
