from powershame import app
from powershame import db
from powershame import models
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
    token = db.Column( db.Unicode(256), index=True ) #TODO: index this
    user = db.Column( db.Integer, db.ForeignKey('user.id') )
    name = db.Column( db.Unicode(256) )
    valid = db.Column( db.Boolean )
    os = db.Column( db.Integer )
    date_authorized = db.Column( db.DateTime )

    def serialize( self ):
        return {
            'user':     self.get_user().username,
            'name':     self.name,
            'valid':    self.valid,
            'token':    self.token
        }

    def verify(self):
        user = self.get_user()
        return pbkdf2_sha512.verify( user.password, self.token )

    def get_user(self):
        return models.user.load_user( self.user )

    def __repr__(self):
        return '%(name)s (%(user)s)' % { 'name':str(self.name), 'user': str(self.get_user()) }

def get_client_by_token( token ):
    return Client.query.filter_by(token=token).first() or None
