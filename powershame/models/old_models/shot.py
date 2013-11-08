from powershame import app
from powershame import db
from powershame.models.upload_form import UploadForm


class Shot(db.Model):
    id   = db.Column( db.Integer, primary_key=True )
    user = db.Column( db.Integer, db.ForeignKey('user.id') )
    client = db.Column( db.Integer, db.ForeignKey('client.id') )
    time = db.Column( db.Float, index=True )
    user =      db.Column( 'user', db.Integer, db.ForeignKey('user.id'), index=True )
    upload_form = db.Column( 'upload_form', db.Integer, db.ForeignKey('upload_form.id'), index=True )

def create_or_update_shot( user, client, time ):
    shot =  Shot.query.filter( user==user, client==client, time==time ).first() \
            or \
            Shot( user=user, client=client, time=time ) 
    if shot.upload_form:
        UploadForm.get( shot.upload_form ).invalidate()

