import json
from powershame import db, app
from powershame.models.user import User
from boto.s3.connection import S3Connection

conn = S3Connection( app.config['ISSUER_KEY'], app.config['ISSUER_SECRET'] )

class Screenshot( db.Model ):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column( db.Integer, db.ForeignKey('user.id'), index=True )
    time = db.Column( db.BigInteger, index=True )
    upload_args = db.Column( db.Unicode(2048) )

    def serialize( self ):
        serial = dict( (x,getattr(self,x) ) for x in ('id','time','upload_args') )
        serial['user'] = User.query.get( self.user ).email
        return serial

    def render_serialize( self ):
        serial = dict( (x,getattr(self,x) ) for x in ('id','time','user') )
        serial['key'] = self.get_key()
        return serial

    def get_upload_args( self ):
        global conn
        form_args = conn.build_post_form_args(
                app.config['PIC_BUCKET'], 
                max_content_length = app.config['MAX_PIC_SIZE'],
                key = self.get_key() )
        self.upload_args = json.dumps( form_args )
        db.session.add( self )
        db.session.commit()
        return form_args

    def get_key( self ):
        return "%d/%d.png" % ( self.user, self.id )
