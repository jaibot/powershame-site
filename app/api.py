from flask import request, abort, jsonify

from app import app
from app import db
from app import login_manager
from app import models
from app import forms

from app.permission_generator import get_temp_upload_creds
from models.user import User, get_by_token
from models.token import Token
from models.session import Session

import requests
from werkzeug.datastructures import MultiDict

@app.route('/get_token', methods = ['POST'])
def get_token():
    if not request.json or not 'password' in request.json:
        abort(400)
    username=request.json['username']
    password=request.json['password']
    user =  User.query.filter_by(username=username).first()
    if not user:
        return jsonify( {'error': 'no such user' } )
    if user.check_pw( password ):
        token = Token( user )
        return jsonify( { 'token': token.id } ), 201
    else:
        return jsonify( { 'error': 'invalid password' } )

#@app.route('/start_session', methods = ['POST'] )
#def start_session():
#    if not request.json or not 'token' in request.json:
#        abort(400)
#    user = get_by_token( request.json['token'] )
#    session = Session( user )
#    return jsonify( {'id': session.id } )

@app.route('/get_s3_permissions', methods = ['POST'] )
def get_s3_permissions():
    if not request.json or not 'token' in request.json:
        abort(400)
    user = get_by_token( request.json['token'] )
    if user: #only authorize real sessions
        creds = get_temp_upload_creds( user.username ) #TODO: change prefix
        return jsonify( {   'access_key':   creds.access_key,
                            'secret_key':   creds.secret_key,
                            'session_token':creds.session_token,
                            'prefix'    :   user.username } )
    abort(400)

@app.route('/session_complete', methods = ['POST'])
def session_complete():
    """convenience function - return username corresponding to token if it exists"""
    if not request.json or not 'token' in request.json or not 'session_name' in request.json:
        abort(400)
    user = get_by_token( request.json['token'] )
    if user:
        prefix = user.username + '/' + request.json['session_name']
        if Session.query.filter_by( prefix=prefix ).first():
            return jsonify( {'status' : 'duplicate'} )
        else:
            session = Session( user.id, prefix )
            return jsonify( {   'status' : 'success' } )
    else:
        abort(400)

@app.route('/verify_token', methods = ['POST'])
def verify_token():
    """API interface for completing session"""
    if not request.json or not 'token' in request.json:
        abort(400)
    user = get_by_token( request.json['token'] )
    if user:
        return jsonify( {'user' : user.username} )
    else:
        abort(400)

@app.route('/status', methods = ['POST'])
def get_status():
    return jsonify( {'status': 'alive'} )
