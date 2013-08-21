from app import app
from app import db

session_shamers = db.Table( 
    'session_shamers',
    db.Column( 'session', db.Integer, db.ForeignKey('session.id') ),
    db.Column( 'shamer', db.Integer, db.ForeignKey('contact_info.id') )
)
