from powershame import db

class Shamer( db.Model ):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column( db.Integer, db.ForeignKey('user.id'), index=True )
    email = db.Column( db.Unicode( 512 ) )
    confirmed = db.Column( db.Boolean, default=False )
    db.UniqueConstraint( 'user','email' )
