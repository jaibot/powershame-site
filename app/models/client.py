from app import app
from app import db
from app import models
from passlib.hash import pbkdf2_sha512
from datetime import datetime

class Client(db.Model):
    """The client class representing machines authorized on a user account

    Tokens are generated from a hash of the user's password hash. This ensures
    that if the user changes their password, all of their existing authorizations
    will be invalid

    TODO delete existing tokens on password change
    """
    id = db.Column(db.Integer, primary_key = True)
    token = db.Column( db.String(256), index=True ) #TODO: index this
    user = db.Column( db.Integer, db.ForeignKey('user.id') )
    name = db.Column( db.String(256) )
    valid = db.Column( db.Boolean )
    date_authorized = db.Column( db.DateTime )
    def __init__( self, user, name=None ):
        self.user = user.id
        self.token = pbkdf2_sha512.encrypt( user.password )
        if name:
            self.name = name
        else:
            self.name = 'Unnamed Client'
        self.valid = True
        self.date_authorized = datetime.now()
        db.session.add(self)
        db.session.commit()

    def serialize( self ):
        return {
            'user':     models.user.load_user( self.user ).username,
            'name':     self.name,
            'valid':    self.valid,
            'token':    self.token
        }

    def verify(self):
        user = load_user( self.user )
        return pbkdf2_sha512.verify( self.token, user.password )

    def get_user(self):
        return models.user.load_user( self.user )

    def __repr__(self):
        return '%(name)s (%(user)s)' % { 'name':str(self.name), 'user': str(self.get_user()) }

def get_client_by_token( token ):
    return Client.query.filter(token=token).first() or None
