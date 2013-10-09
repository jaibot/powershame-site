from powershame import app
from powershame import db
from powershame import login_manager
from powershame.models.client import Client
from powershame.models.upload_creds import UploadCreds
from powershame.models.contact_info import ContactInfo
from powershame.models.user_shamers import user_shamers
from passlib.hash import pbkdf2_sha512

shamers = db.Table('shamers',
    db.Column('user', db.Integer, db.ForeignKey('user.id'), primary_key=True ),
    db.Column('shamer', db.Integer, db.ForeignKey('user.id'), primary_key=True )
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Unicode(32), unique = True, index=True)
    password = db.Column(db.Unicode(130))
    is_registered = db.Column( db.Boolean )
    clients = db.relationship('Client', backref = 'owner', lazy = 'dynamic')
    sessions = db.relationship('Session', backref = 'owner', lazy = 'dynamic')
    upload_creds = db.relationship('UploadCreds', backref = 'owner', lazy = 'dynamic')
    contact_info = db.relationship('ContactInfo', backref = 'user', lazy='dynamic')
    shamers = db.relationship('ContactInfo', secondary=user_shamers,  backref='shamee', lazy='dynamic' )

    def __init__( self, username, pw, email=None ):
        if self.query.filter_by( username=username ).first():
            raise UsernameExists
        self.username = username
        self.password = pbkdf2_sha512.encrypt( pw )
        self.is_registered = True
        db.session.add(self)
        db.session.commit()
        email_contact = ContactInfo( self, email, ContactInfo.EMAIL )
        db.session.add(email_contact)
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

    def get_upload_creds( self ):
        """Return a good credential (if it exists) or None"""
        creds = self.upload_creds.all()
        for c in creds:
            if c.expired():
                db.session.delete( c )
        db.session.commit( )
        creds = self.upload_creds.first() or UploadCreds( self )
        return creds

    def can_add_client( self ):
        return len( self.clients.all() ) < app.config['MAX_CLIENTS_PER_USER']

    def __repr__(self):
        return 'User: %(username)s' % {'username': self.username} 

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def name_exists( name ):
    return User.query.filter_by(username=name).first() is not None

def get_user_by_token( token_string ):
    token = Client.query.filter_by( token = token_string ).first()
    if token:
        return load_user( token.user )
    else:
        return None

def get_user_by_login( username, password ):
    """Return user corresponding to correct username/pw combination or None """
    user = User.query.filter_by( username = username ).first()
    if user and user.check_pw( password ):
        return user
    return None

class UsernameExists( Exception ):
    pass
