from app import app
from app import db


class Shot(db.Model):
    id   = db.Column( db.Integer, primary_key=True )
    user = db.Column( db.Integer, db.ForeignKey('user.id') )
    source = db.Column( db.Integer, db.ForeignKey('client.id') )
    time = db.Column( db.Float, index=True )
    key = db.Column( db.Unicode(128) )

