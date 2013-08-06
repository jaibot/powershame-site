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

FAIL,OK=0,1

def create_user( username, password ):
    try:
        user = User( username, password )
    finally:
        return SUCCESS

def delete_user( user ):
    pass #TODO

def set_password( user, password ):
    pass #TODO

def create_session( user, name ):
    pass #TODO

def complete_session( user, name ):
    return OK, None

def create_token( user ):
    pass #TODO

def add_client( user, name ):
    """create client"""
    client = Client( user, name )
    return OK, client

def get_client_token( user, client ):
    """get token corresponding to client"""
    pass #TODO

def delete_client( user, client ):
    pass #TODO

def check_token( user, token ):
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
    if cred.expired():
        return new_upload_creds( user )
    else:
        return creds

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


