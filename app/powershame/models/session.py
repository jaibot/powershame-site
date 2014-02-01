from powershame import db, app
from powershame.models.user import User
import time

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
    description = db.Column( db.Unicode(4096) )

    def serialize( self ):
        serial = dict( (x,getattr(self,x) ) for x in ('id','start','end', 'height', 'width') )
        serial['user'] = User.query.get( self.user ).email
        return serial

    def pretty_time( self ):
        """Hacky fix for time display - TODO: proper jinja filter later"""
        if not (self.start and self.end):
            return "Incomplete session"
        day_str = time.strftime( '%b %d, %Y', time.localtime(self.start) )
        start_str = time.strftime( '%I:%M %P', time.localtime( self.start) )
        end_str = time.strftime( '%I:%M %P', time.localtime( self.end) )
        return day_str + ': ' + start_str + ' - ' + end_str

