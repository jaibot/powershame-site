from app import app
from app import db

user_shamers = db.Table( 
    'user_shamers',
    db.Column( 'user', db.Integer, db.ForeignKey('user.id') ),
    db.Column( 'shamer', db.Integer, db.ForeignKey('contact_info.id') )
)
