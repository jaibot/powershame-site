from app import app
from app import db
from app.models.user import load_user
import datetime

class Session(db.Model):
    """The Session class representing a single powershame session

    Tokens are generated from a hash of the user's password hash. This ensures
    that if the user changes their password, all of their existing authorizations
    will be invalid

    TODO delete existing tokens on password change
    """
    id   = db.Column( db.Integer, primary_key=True )
    name = db.Column(db.Unicode(256) )
    user = db.Column( db.Integer, db.ForeignKey('user.id') )
    source = db.Column( db.Integer, db.ForeignKey('client.id') )
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    def __init__( self, user_id, name ):
        self.user = user_id
        self.name = name
        self.user_id = user_id
        db.session.add(self)
        db.session.commit()
    def age_in_seconds(self):
        return (datetime.datetime.now()-self.start_time).seconds
    def __repr__(self):
        return '%(name)s (%(user)s)' % {'name': self.name, 'user': str(load_user( self.user )) }
