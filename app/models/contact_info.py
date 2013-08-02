from app import app
from app import db

class ContactInfo(db.Model):
    """"""
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    contact_type = db.Column(db.SmallInteger)
    identifier = db.Column( db.String(512) )
    def __init__( self, user_id, shamer_id ):
        self.user_id = user_id
        self.shamer_id = shamer_id
        db.session.add(self)
        db.session.commit()
