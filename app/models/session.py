from app import app
from app import db
from random import Random
from string import letters,digits
import datetime

class Session(db.Model):
    """The Session class representing a single powershame session

    Tokens are generated from a hash of the user's password hash. This ensures
    that if the user changes their password, all of their existing authorizations
    will be invalid

    TODO delete existing tokens on password change
    """
    id = db.Column(db.Unicode(256), primary_key=True )
    prefix = db.Column(db.Unicode(256) )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime)
    def __init__( self, user ):
        self.id = self.make_id()
        self.user_id = user.id
        self.prefix = self.make_prefix( user.username )
        self.start_time = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()
    def make_id( self ):
        r = Random()
        r.seed()
        return ''.join( r.choice( letters+digits ) for x in xrange(256) )
    def make_prefix( self, username ):
        return '/'.join(( username, now_str() ))
    def age_in_seconds(self):
        return (datetime.datetime.now()-self.start_time).seconds
    def __repr__(self):
        return self.prefix

def now_str():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

