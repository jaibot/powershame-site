from app import db
from app import app
from app import login_manager 
from passlib.hash import pbkdf2_sha512
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Unicode(32), unique = True)
    password = db.Column(db.Unicode(130))

    def __init__( self, username, pw ):
        self.username = username
        self.password = pbkdf2_sha512.encrypt( pw )
        db.session.add(self)
        db.session.commit()
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
        return False

    def get_id(self):
        return unicode(self.id)
    
    def check_pw( self, pw ):
        return pbkdf2_sha512.verify( pw, self.password )

    def set_pw( self, pw ):
        self.password = hash_pw( pw )

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def name_exists( name ):
    return User.query.filter_by(username=name).first() is not None

#HTTPAuth stuff for API -TODO move this somewhere else later 
@auth.get_password
def get_password(username):
    user =  User.query.filter_by(username=name).first()
    if user is not None:
        return user.password
#TODO handle no password case

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)
