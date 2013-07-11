from app import db
from app import app
from app import login_manager 

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique = True)
    password = db.Column(db.String(64))
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
        return False

    def get_id(self):
        return unicode(self.id)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
