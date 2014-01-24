from powershame import db, app
from powershame.models.user import User

class Session( db.Model ):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column( db.Integer, db.ForeignKey('user.id'), index=True )
    start = db.Column( db.BigInteger, index=True )
    end = db.Column( db.BigInteger, index=True )
    rendered = db.Column( db.Boolean, default=False )
    secret = db.Column( db.Unicode(64) )
    key = db.Column( db.Unicode( 64 ) )
    bucket = db.Column( db.Unicode(64) )
    width = db.Column( db.Integer , default=800)
    height = db.Column( db.Integer , default=450)

    def serialize( self ):
        serial = dict( (x,getattr(self,x) ) for x in ('id','start','end', 'height', 'width') )
        serial['user'] = User.query.get( self.user ).email
        return serial
