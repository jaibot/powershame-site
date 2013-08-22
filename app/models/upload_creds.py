from app import db
from app import app
from app.permission_generator import get_temp_upload_creds
from datetime import datetime, timedelta

class UploadCreds(db.Model):
    __tablename__='upload_creds'
    id =        db.Column( 'id', db.Integer, primary_key=True )
    user =      db.Column( 'user', db.Integer, db.ForeignKey('user.id'), index=True )
    expiration= db.Column( 'expiration', db.DateTime )
    access_id = db.Column( 'access_id', db.String(256) )
    secret_key = db.Column( 'secret_key', db.String(256) )
    session_token = db.Column( 'session_token', db.String(2048) )
    prefix      = db.Column( 'prefix', db.String(256) )

    # We may either pass accessid+key+token+expiration, or generate them given only user
    def __init__(   self, 
                    user,
                    duration = None,
                    access_id = None,
                    secret_key = None,
                    session_token = None,
                    expiration = None ):
        # Although user and prefix are currently redundant, I may change prefix later
        self.user = user.id
        self.prefix = str(user.id)+u'/'
        if all( (access_id, secret_key, session_token, expiration) ):
            self.access_id = access_id
            self.secret_key = secret_key
            self.session_token = session_token
            self.expiration = expiration
        else:
            # AWS doesn't return an expiration time, so we have to estimate
            # based on what we pass it. This should be accurate to within a few seconds,
            # but I start the clock before making the request anyway. This may mean
            # there are times when I think the creds are expired but they're still
            # good for a few more seconds, but that's fine
            if not duration:
                duration = app.config['UPLOAD_CREDS_LIFETIME']
            self.expiration = expiration or datetime.now()+timedelta( seconds=duration )
            try:
                credential = get_temp_upload_creds( prefix=self.prefix, lifetime = duration )
                #TODO: sane error handling
            except:
                return None
            self.access_id = credential.access_key
            self.secret_key = credential.secret_key
            self.session_token = credential.session_token
        db.session.add( self )
        db.session.commit()
    def expired( self ):
        return datetime.now() > self.expiration
    def serialize( self ):
        return {
                'user':         self.user,
                'prefix':       self.prefix,
                'access_key':   self.access_id,
                'secret_key':   self.secret_key,
                'session_token':self.session_token,
                'expiration':   str(self.expiration)
            }
    def __repr__( self ):
        return str( self.serialize() )

