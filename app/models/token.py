from app import app
from app import db
from app.models.user import load_user
from passlib.hash import pbkdf2_sha512
#from models.user import load_user

class Token(db.Model):
    """The token class representing authorization codes on user accounts

    Tokens are generated from a hash of the user's password hash. This ensures
    that if the user changes their password, all of their existing authorizations
    will be invalid

    TODO delete existing tokens on password change
    """
    id = db.Column(db.String(256), primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__( self, user ):
        self.user_id = user.id
        self.id = pbkdf2_sha512.encrypt( user.password )
        db.session.add(self)
        db.session.commit()

    def verify(self):
        user = load_user( self.user_id )
        return pbkdf2_sha512.verify( self.id, user.password )

    def get_user(self):
        return app.models.user.load_user( self.id )

    def __repr__(self):
        return self.id
