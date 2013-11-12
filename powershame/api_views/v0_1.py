import os
VERSION = 'v0.1'
API_URL = '/api/'+VERSION

from flask import request, jsonify, url_for
from flask.ext.restful import Resource, reqparse

from powershame import app, db, api
from powershame.httpcodes import HTTPCode

from powershame.models.user import User
from powershame.models.screenshots import Screenshot
from powershame.models.session import Session
from powershame import jobs

from time import time
from functools import wraps

from boto.s3.connection import S3Connection
from boto.s3.key import Key

conn = S3Connection( app.config['ISSUER_KEY'], app.config['ISSUER_SECRET'] )

def api_error_factory( code, default_message=None ):
    def some_error( message=default_message ):
        response = jsonify({'message':message, 'code': code} )
        response.status_code = code
        return response
    return some_error
bad_request = api_error_factory( HTTPCode.BAD_REQUEST )
unauthorized = api_error_factory( HTTPCode.UNAUTHORIZED )
denied = api_error_factory( HTTPCode.DENIED )
slow_down = api_error_factory( HTTPCode.TOO_MANY_REQUESTS )
not_found = api_error_factory( HTTPCode.NOT_FOUND )

def auth_required(f):
    """Decorator for functions requiring a valid token"""
    @wraps(f)
    def authed_f(*args, **kwargs):
        for x in ('username', 'API-Token'):
            if not (x in request.headers and request.headers[x]):
                return bad_request("Missing required header %s"%x)
        token = request.headers['API-Token']
        user = User.query.filter_by(email=request.headers['username']).first()
        if not user:
            return bad_request('No user specified')
        if not user.check_auth_token( token ):
            return unauthorized("Invalid token")
        kwargs['user'] = user
        return f(*args, **kwargs)
    return authed_f

def throttle(f):
    """Decorator for functions to be throttled per-user"""
    def throttled_f( *args, **kwargs ):
        for x in ('username', 'API-Token'):
            if not (x in request.headers and request.headers[x]):
                return bad_request("Missing required header %s"%x)
        user = User.query.filter_by(email=request.headers['username']).first()
        # calls are forgiven every THROTTLE_DECAY seconds, 
        #   so calculate how many user has earned since last call
        if not user:
            return bad_request('No user specified')
        if not user.last_throttle_check:
            user.last_throttle_check = int(time() )
        if not user.throttle_counter:
            user.throttle_counter=0
        time_passed = int( time() - (user.last_throttle_check or 1) )
        credits_earned = time_passed/(app.config['THROTTLE_DECAY'])
        # give the user their time credit, deducting 1 (for this call)
        user.throttle_counter = max( 1, user.throttle_counter-credits_earned+1 )
        # only update for time that counted towards throttle decay
        user.last_throttle_check += (credits_earned*app.config['THROTTLE_DECAY'] )
        if user.throttle_counter > app.config['THROTTLE_MAX_CALLS']:
            return slow_down("You're making too many requests")
        return f(*args, **kwargs)
    return throttled_f

class TokenApi( Resource ):
    url = API_URL + '/token'
    def __init__( self ):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument( 'username', type=str, required=True,
                help = "No user specified", location='json' )
        self.post_parser.add_argument( 'password', type=str, required=True,
                help = "password required", location='json' )
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument( 'username', type=str, required=True,
                help = "No username specified" )
        self.get_parser.add_argument( 'token', type=str, required=True,
                help = "No token specified" )
        super( TokenApi, self).__init__()
    def post( self ):
        args = self.post_parser.parse_args()
        user = User.query.filter_by(email=args['username']).first()
        if user:
            return {    'token': user.get_auth_token(),
                        'username': user.email  }
        else:
            return bad_request()
                
    def get( self ):
        args = self.get_parser.parse_args()
        user = User.query.filter_by(email=args['username']).first()
        token = args['token']
        return { 'valid': user.check_auth_token( token ) }

class ScreenshotApi( Resource ):
    url = API_URL+'/screenshot'
    decorators = [ auth_required, throttle ]
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('time', type = int, required = True,
            help = 'No time provided' )
        super(ScreenshotApi, self).__init__()   

    def post( self, user ):
        args = self.post_parser.parse_args()
        time = args['time']
        s = Screenshot.query.filter_by( user=user.id, time=time ).first()
        if not s:
            s = Screenshot( time=time, user=user.id )
        db.session.add(s)
        db.session.commit()
        upload_args = s.get_upload_args()
        return upload_args

class SessionListApi( Resource ):
    url = API_URL+'/session_list'
    decorators = [ auth_required, throttle ]

    def post( self, user=None ):
        session = Session( user=user.id )
        db.session.add( session )
        db.session.commit()
        return serialize_with_url( session )
    def get( self, user=None ):
        return { 'sessions': ( serialize_with_url(s) for s in user.sessions ) }

def serialize_with_url( session ):
    serial = session.serialize()
    serial['url'] = _session_url( session )
    return serial

def _session_url( session ):
    return api.url_for(SessionApi, id=session.id, _external=True)

class SessionApi( Resource ):
    url = API_URL+'/session/<int:id>'
    decorators = [ auth_required, throttle ]

    def __init__( self ):
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument( 'start', type = int )
        self.put_parser.add_argument( 'end', type = int )
        super( SessionApi, self ).__init__()

    def put( self, id, user ):
        args = self.put_parser.parse_args()
        session = Session.query.get( id )
        db.session.add( session )
        for k,v in args.iteritems():
            if v:
                setattr( session, k, v )
        db.session.commit()
        if args['end']:
            jobs.render( session )
        return serialize_with_url( session )

class RenderApi( Resource ):
    url = API_URL+'/render/<int:id>'
    def __init__( self ):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument( 'secret', type=str, required=True )
    def post( self, id ):
        args = self.post_parser.parse_args()
        session = Session.query.get( id )
        if args['secret'] != session.secret:
            return unauthorized()
        jobs.post_render( id ) #TODO: offload this to celery async task
        return 200

api.add_resource(TokenApi, TokenApi.url, endpoint = 'token_api')
api.add_resource(ScreenshotApi, ScreenshotApi.url, endpoint = 'screenshot_api')
api.add_resource(SessionListApi, SessionListApi.url, endpoint='session_list_api')
api.add_resource(RenderApi, RenderApi.url, endpoint = 'render_api' )
api.add_resource(SessionApi, SessionApi.url, endpoint='session_api')
