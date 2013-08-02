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
    prefix = db.Column(db.Unicode(256), primary_key=True )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    def __init__( self, user_id, prefix ):
        self.prefix = prefix
        self.user_id = user_id
        self.start_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now() #TODO: actual times
        db.session.add(self)
        db.session.commit()
    def make_id( self ):
        r = Random()
        r.seed()
        return ''.join( r.choice( letters+digits ) for x in xrange(256) )
    def age_in_seconds(self):
        return (datetime.datetime.now()-self.start_time).seconds
    def __repr__(self):
        return self.prefix

def now_str():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

