from app import db
from app import app
from datetime import datetime

class UploadCreds(db.Model):
    __tablename__='upload_creds'
    id =        db.Column( 'id', db.Integer, primary_key=True )
    user =      db.Column( 'user', db.Integer, db.ForeignKey('user.id'), index=True )
    expiration= db.Column( 'expiration', db.DateTime )
    access_id = db.Column( 'access_id', db.String(256) )
    secret_key = db.Column( 'secret_key', db.String(256) )
    session_token = db.Column( 'session_token', db.String(2048) )
    prefix      = db.Column( 'prefix', db.String(256) )
    def __init__(   self, 
                    user, 
                    expiration,
                    access_id,
                    secret_key,
                    session_token ):
        self.user = user.id
        self.expiration = expiration
        self.access_id = access_id
        self.secret_key = secret_key
        self.session_token = session_token
        self.prefix = user.username + '/'
        db.session.add( self )
        db.session.commit()
    def expired( self ):
        return datetime.now() > self.expiration
    


