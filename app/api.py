from app import app
from app import db
from app import controller
from controller import add_client, OK,FAIL, complete_session
from app.models.user import User, get_user_by_token, get_user_by_login
from app.models.client import Client

from flask import request, abort, jsonify
import requests
from werkzeug.datastructures import MultiDict


def valid_request( request, vars ):
    print request.json
    print vars
    print all( v in request.json for v in vars)
    return request.json and all( v in request.json for v in vars )

def compose_response( result=OK, message=None, args=None ):
    response=dict()
    if args:
        response=args.copy()
    if result==OK:
        response['result']='OK'
    elif result==FAIL:
        response['result']='FAIL'
    else:
        response['result']='UNKNOWN' #TODO: Raise a red flag
    if message:
        response['message']=message
    return jsonify(response)

def api_login(request):
    if not request.json:
        return None
    if 'token' in request.json:
        return get_user_by_token( request.json['token'] )
    elif 'username' in request.json and 'password' in request.json:
        return get_user_by_login( request.json['username'], request.json['password'] )
    else:
        return None

@app.route('/add_client', methods = ['POST'])
def add_client():
    """Given a name and either a working token or u/p, add client and return token"""
    if valid_request( request, ('client_name',) ):
        user = api_login( request )
        if user:
            if 'name' in request.json:
                name = request.json['name']
            else:
                name = "Unnamed client"
            status,new_client = add_client( user, name )
            if status==OK:
                return compose_response( OK, args={'token': new_client.token} )
            else:
                return compose_response( OK, message='Could not add client' )
        else:
            return compose_response( FAIL, message='Invalid login' )
    else:
        return compose_response( FAIL, message='No client name given' )

@app.route('/get_token', methods = ['POST']) #legacy - TODO: delete (after updating client)
def get_token():
    return add_client()

@app.route('/get_s3_permissions', methods = ['POST'] )
def get_s3_permissions():
    if valid_request( request, ('token',) ):
        user = get_user_by_token( request.json['token'] )
        if user:
            creds = user.get_upload_creds()
            return compose_response( OK, args= {   
                    'access_key':   creds.access_id,
                    'secret_key':   creds.secret_key,
                    'session_token':creds.session_token,
                    'prefix':       creds.prefix} )
        else:
            return compose_response( FAIL, message="Invalid token" )
    else:
        return compose_response( FAIL, message="No token given" )

@app.route('/session_complete', methods = ['POST'])
def session_complete():
    if valid_request( request, ('token', 'session_name') ):
        user = get_user_by_token( request.json['token'] )
        status, session = complete_session( user, request.json['session_name'] ) #TODO
        return compose_response( status )
    else:
        return compose_response( FAIL, message="Invalid token or session_name" )

@app.route('/verify_token', methods = ['POST'])
def verify_token():
    """API interface for completing session"""
    if valid_request( request, ('token',) ):
        user = get_user_by_token( request.json['token'] )
        if user:
            return compose_response( OK, args={'user': user.username} )
        else:
            return compose_response( FAIL, message="Invalid token or user" )
    else:
        return compose_response( FAIL, message="Invalid request" )

@app.route('/status', methods = ['POST'])
def get_status():
    return compose_response( OK, args={'status':'alive'}  )
