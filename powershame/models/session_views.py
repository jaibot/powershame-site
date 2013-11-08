from powershame import db
from powershame.models.session import Session
from powershame.models.shamers import Shamer

class SessionView( db.Model ):
    id = db.Column( 'id', db.Integer, primary_key=True )
    session_id = db.Column( 'session', db.Integer, db.ForeignKey('session.id'), index=True )
    shamer_id = db.Column( 'shamer', db.Integer, db.ForeignKey('shamer.id'), index=True )
    secret = db.Column( 'secret', db.Unicode(64), unique=True, index=True )
    
    session = db.relationship( Session, backref='session_views' )
    shamer = db.relationship( Shamer, backref='shamer' )
