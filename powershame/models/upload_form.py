from powershame import db
from powershame import app
from boto.s3.connection import S3Connection
import time

def get_upload_form_args( filename, user_id ):
    conn = S3Connection( app.config['ISSUER_KEY'], app.config['ISSUER_SECRET'] )
    form_args = conn.build_post_form_args(
            app.config['PIC_BUCKET'], 
            filename, 
            max_content_length = app.config['MAX_PIC_SIZE'],
            key = "%d/${filename}" % user_id )
    return form_args

class UploadForm(db.Model):
    __tablename__='upload_form'
    id =        db.Column( 'id', db.Integer, primary_key=True )
    user =      db.Column( 'user', db.Integer, db.ForeignKey('user.id'), index=True )
    time_issued = db.Column( 'date_issued', db.Time )
    def get_form_args( self ):
        self.time_issued = time.time()
        return get_upload_url( self.filename, self.user )
