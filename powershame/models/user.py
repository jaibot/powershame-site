from flask.ext.login import UserMixin
from powershame import db, login_manager
from passlib.hash import pbkdf2_sha512

def int_time():
    return int( time() )

class User( db.Model, UserMixin ):
    id = db.Column(db.Integer, primary_key = True)
    email  = db.Column(db.Unicode(255), unique = True, index=True)
    password = db.Column(db.Unicode(255))
    throttle_counter = db.Column( db.SmallInteger )
    last_throttle_check = db.Column( db.Integer, default=int_time )
    last_login_at = db.Column( db.DateTime )
    current_login_at = db.Column( db.DateTime )
    last_login_ip = db.Column( db.Unicode(30) )
    current_login_ip = db.Column( db.Unicode(30) )
    login_count = db.Column( db.Integer )
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    screenshots = db.relationship('Screenshot', backref = 'owner', lazy = 'dynamic' )
    sessions = db.relationship('Session', backref = 'owner', lazy = 'dynamic')
    shamers = db.relationship('Shamer', backref = 'shamee', lazy = 'dynamic')

    def __init__( self, password, **kwargs ):
        self.password = pbkdf2_sha512.encrypt( password )
        db.Model.__init__( self, **kwargs )

    def set_password( self, pw ):
        self.password = pbkdf2_sha512.encrypt( pw )

    def check_pw( self, pw ):
        return pbkdf2_sha512.verify( pw, self.password )

    def get_auth_token( self ):
        """tokens are generated from encrypted password"""
        return pbkdf2_sha512.encrypt( self.password )

    def check_auth_token( self, token ):
        """check that password was used to generate token"""
        return pbkdf2_sha512.verify( self.password, token )

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

def get_user_by_login( email, password ):
    """Return user corresponding to correct email/pw combination or None """
    user = User.query.filter_by( email = email ).first()
    if user and user.check_pw( password ):
        return user
    return None
