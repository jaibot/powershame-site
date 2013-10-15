from powershame import db
from powershame import app
from powershame.permission_generator import get_temp_upload_creds
import time

class UploadCreds(db.Model):
    __tablename__='upload_creds'
    id =        db.Column( 'id', db.Integer, primary_key=True )
    user =      db.Column( 'user', db.Integer, db.ForeignKey('user.id'), index=True )

    # We may either pass accessid+key+token+expiration, or generate them given only user
    #def __init__(   self, 
    #                user,
    #                duration = None,
    #                access_id = None,
    #                secret_key = None,
    #                session_token = None,
    #                expiration = None ):
    #    # Although user and prefix are currently redundant, I may change prefix later
    #    self.user = user.id
    #    self.prefix = str(user.id)+u'/'
    #    if all( (access_id, secret_key, session_token, expiration) ):
    #        self.access_id = access_id
    #        self.secret_key = secret_key
    #        self.session_token = session_token
    #        self.expiration = expiration
    #    else:
    #        # AWS doesn't return an expiration time, so we have to estimate
    #        # based on what we pass it. This should be accurate to within a few seconds,
    #        # but I start the clock before making the request anyway. This may mean
    #        # there are times when I think the creds are expired but they're still
    #        # good for a few more seconds, but that's fine
    #        if not duration:
    #            duration = app.config['UPLOAD_CREDS_LIFETIME']
    #        self.expiration = expiration or ( time.time() + duration )
    #        credential = get_temp_upload_creds( prefix=self.prefix, lifetime = duration )
    #        self.access_id = credential.access_key
    #        self.secret_key = credential.secret_key
    #        self.session_token = credential.session_token
    #    db.session.add( self )
    #    db.session.commit()
    #def expired( self ):
    #    print time.time()
    #    print self.expiration
    #    print time.time() > self.expiration
    #    if self.expiration:
    #        return time.time() > self.expiration
    #    return True
    def serialize( self ):
        return {
                'user':         self.user,
            }
    def __repr__( self ):
        return str( self.serialize() )

