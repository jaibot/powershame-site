from app import app
from app import db

class ContactInfo(db.Model):
    """"""
    __tablename__='contact_info'
    id = db.Column(db.Integer, primary_key=True )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    contact_type = db.Column(db.SmallInteger)
    identifier = db.Column( db.String(512) )
    EMAIL=0
    def __init__( self, user, identifier, contact_type=EMAIL ):
        self.user_id = user.id
        self.identifier = identifier
        self.contact_type = contact_type
        db.session.add(self)
        db.session.commit()
