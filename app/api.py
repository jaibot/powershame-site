#TODO: UGH, lots of things to fix
from app import app
from app import db
from app import controller
from controller import OK,FAIL
from app.models.user import User, get_user_by_token, get_user_by_login
from app.models.client import Client, get_client_by_token
from app.models.session import Session

from flask import request, abort, jsonify
import requests
from werkzeug.datastructures import MultiDict
from functools import wraps

import logging

class HTTPCode:
    ok = 200
    bad_request=400
    unauthorized=401
    denied = 403
    server_error = 500

def auth_required(f):
    """Decorator for functions rewuiring a valid token"""
    @wraps(f)
    def authed_f(*args, **kwargs):
        token_header=app.config['API_TOKEN_HEADER']
        if not token_header in request.headers:
            return jsonify({'message':'Header missing: %s'%token_header}), HTTPCode.unauthorized
        token = request.headers[token_header]
        client=get_client_by_token( token )
        if not client or not client.verify():
            return jsonify({'message':'Invalid token'}), HTTPCode.unauthorized
        kwargs['client'] = client
        kwargs['user']= client.owner
        return f(*args, **kwargs)
    return authed_f

def api(required=None):
    """Decorator for API functions ensuring sanity and required arguments"""
    def make_wrap(f):
        @wraps(f)
        def apied_f( *args, **kwargs ):
            try:
                if not request.json:
                    return jsonify({'message':'Request must be in JSON format'}),HTTPCode.bad_request
                if required and not all( r in request.json for r in required ):
                    response = dict( (r,r in request.json) for r in required )
                    response['message'] = 'One or more required arguments missing'
                    return jsonify(response), HTTPCode.bad_request
                return f(*args, **kwargs)
            except Exception as e:
                logging.critical(str(e), exc_info=1)
                return jsonify({'message':'Something went horribly wrong'}),HTTPCode.server_error
                #TODO: Log and alert whatever disaster just happened
        return apied_f
    return make_wrap

@app.route('/api/status', methods = ['GET'])
def status(*args, **kwargs):
    return jsonify({'message':'I feel happy!'}),HTTPCode.ok

@app.route('/api/check_auth_token', methods = ['GET'])
@auth_required
def verify_token( *args, **kwargs):
    return jsonify({'message':'Token is valid.'}),HTTPCode.ok

@app.route('/api/register_client', methods = ['POST'])
@api(required=('username','password','client_name'))
def register_client( *args, **kwargs ):
    username = request.json['username']
    password = request.json['password']
    client_name = request.json['client_name']
    user = get_user_by_login( username, password )
    if user and user.can_add_client():
        client = Client( user, client_name )
    if client:
        return jsonify(client.serialize() ), HTTPCode.ok
    else:
        return jsonify({'message':'Could not create client'}), HTTPCode.denied

@app.route('/api/request_upload_creds', methods = ['POST'])
@api()
@auth_required
def request_upload_creds(*args, **kwargs):
    user = kwargs['user']
    permissions = user.get_upload_creds().serialize()
    if permissions:
        permissions['bucket_name'] = app.config['PIC_BUCKET']
        return jsonify(permissions), HTTPCode.ok
    else:
        return jsonify( {'message':'Could not get credentials'} ), HTTPCode.denied

@app.route('/api/register_session', methods = ['POST'])
@api(required=('name',))
@auth_required
def register_session(*args, **kwargs):
    session_name=request.json['name']
    session = Session( kwargs['user'], session_name, kwargs['client'] )
    return jsonify( session.serialize() ), HTTPCode.ok


@app.route('/api/complete_session', methods=['POST'])
@api()
@auth_required
def complete_session( *args, **kwargs ):
    user=kwargs['user']
    if 'id' in request.json:
        session = Session.query.get( request.json['id'] )
    elif 'name' in request.json:
        name=request.json['name']
        session = _first_or_none( filter(lambda x:x.name==name, user.sessions) )
    else:
        return jsonify( {'message':'Need to supply session id or name'} ), HTTPCode.bad_request
    session.finish()
    return jsonify( {'message':'Session is rendering'} ), HTTPCode.ok 

def _first_or_none(l,n=0):
    if len(l)>n:
        return l[n]
    else:
        return None


