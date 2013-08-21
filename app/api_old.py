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

def api_wrapper( f, required=None ):
    """generic wrapper for all api calls"""
    def f_api( *args, **kwargs ):
        r = kwargs['request']
        try:
            json = r.json
            if required and all( arg in json for arg in required):
                return f( json )
            else:
                missing_args=filter(lambda x: x not in json, required )
                fail_message = 'Missing required arguments %s'%str(missing_args)
                return api_failure( r, 'Missing required arguments' )
        except AttributeError:
            api_failure( r, 'Request must be in JSON format' )
    return f_api

@api_wrapper
def api_token_required( f ):
    """wrapper for API functions requiring token authorization"""
    def f_token( *args, **kwargs):
        json=args[0]
        if not 'token' in json:
            return api_failure( r, 'missing token' )
        client = get_client_by_token( r['token'] )
        if not client:
            return api_failure( r, 'no such token' )
        if not all (token, client, user):
            return api_failure( r, 'lookup failed' )
    return f_token

#def compose_response( result=OK, args=None, message=None ):
#    response=dict()
#    if args:
#        response=args.copy()
#    if result==OK:
#        response['result']='OK'
#    elif result==FAIL:
#        response['result']='FAIL'
#    else:
#        response['result']='UNKNOWN' #TODO: Raise a red flag
#    if message:
#        response['message']=message
#    return jsonify(response)

def api_login(request):
    """return user who made this request"""
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
            new_client = client( user, name ) #TODO: reissue credentials if already exists
            if new_client:
                return compose_response( OK, {'token': new_client.token} )
            else:
                return compose_response( FAIL, message='Could not add client' )
        else:
            return compose_response( FAIL, message='Invalid login' )
    else:
        return compose_response( FAIL, message='No client name given' )

@app.route('/get_token', methods = ['POST']) 
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
                    'prefix':       creds.prefix,
                    'bucket_name':  app.config['PIC_BUCKET']} )
        else:
            return compose_response( FAIL, message="Invalid token" )
    else:
        return compose_response( FAIL, message="No token given" )

@app.route('/session_complete', methods = ['POST'])
def session_complete():
    if valid_request( request, ('token', 'session_name') ):
        client = get_by_token( request.json['token'] )
        user = client.owner
        name = request.json['session_name']
        try:
            session = filter( lambda x: x.name==name, user.sessions )[0]
        except IndexError:
            session = Session( user, name, client )
        if session.status == session.IN_PROGRESS:
            status, session = render_session( session )
            return compose_response( status )
        else:
            if session.status == session.RENDERING:
                return compose_response( FAIL, message='Session is already rendering!' )
            if session.status == session.COMPLETE:
                return compose_response( FAIL, message='Session is already complete!' )
            else:
                return compose_response( FAIL, message='Something has gone terrible wrong.' ) #TODO: handling extremely-wrong things like this.
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
