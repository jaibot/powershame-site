from app import db
from app import app
from app import login_manager 
from app import models
from passlib.hash import pbkdf2_sha512
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

shamers = db.Table('shamers',
    db.Column('user', db.Integer, db.ForeignKey('user.id'), primary_key=True ),
    db.Column('shamer', db.Integer, db.ForeignKey('user.id'), primary_key=True )
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Unicode(32), unique = True)
    password = db.Column(db.Unicode(130))
    is_registered = db.Column( db.Boolean )
    tokens = db.relationship('Token', backref = 'owner', lazy = 'dynamic')
    sessions = db.relationship('Session', backref = 'owner', lazy = 'dynamic')
    #shamers = db.relationship('User', secondary=shamers, backref = db.backref('shamees'), foreign_key )
    shamers = db.relationship('User', secondary=shamers, primaryjoin=id==shamers.c.user, secondaryjoin=id==shamers.c.shamer, backref='shamees' )

    def __init__( self, username, pw, is_registered=True ):
        self.username = username
        self.password = pbkdf2_sha512.encrypt( pw )
        sel.is_registered = is_registered
        db.session.add(self)
        db.session.commit()
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

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

def get_by_token( token_string ):
    print token_string
    token = models.token.Token.query.filter_by( id = token_string ).first()
    print token
    if token:
        return load_user( token.user_id )
    else:
        return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)
