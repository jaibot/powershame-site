from powershame import app
from powershame import db
from powershame.models.user import load_user
from powershame.models.session_shamers import session_shamers
from powershame.messaging import send_message
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
    status = db.Column( db.Integer )
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    url = db.Column( db.Unicode(2048) )
    url_expire = db.Column( db.DateTime )
    shamers = db.relationship('ContactInfo', secondary=session_shamers )
    IN_PROGRESS, RENDERING, FINISHED=1,2,3
    def __init__( self, user, name, client ):
        self.user = user.id
        self.name = name
        self.source = client.id
        self.status = self.IN_PROGRESS
        db.session.add(self)
        db.session.commit()
    def age_in_seconds(self):
        return (datetime.datetime.now()-self.start_time).seconds
    def serialize( self ):
        return {
                'name': self.name,
                'id':   self.id,
                'user': self.user,
                'prefix': str( self.user ) + '/'
            }
    def finish( self, serialized_data ):
        #send_message({'session_id':self.id, }, app.config['RENDERING_QUEUE'] )
        session_data = self.serialize()
        if not all( x['key'].startswith(str(self.user)+'/') for x in serialized_data['screenshots']):
            logging.error('Session contained screenshots not from user')
            return False
        session_data['screenshots'] = serialized_data['screenshots']
        send_message( session_data, app.config['RENDERING_QUEUE'] )
    def post_render( self ):
        pass #TODO #URGENT

    def __repr__(self):
        return '%(name)s (%(user)s)' % {'name': self.name, 'user': str(load_user( self.user )) }
