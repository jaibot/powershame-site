from powershame import app, db, api
from powershame.models.user import User
from powershame.models.session import Session
from powershame.models.session_views import SessionView
from powershame.models.screenshots import Screenshot
from powershame.messaging import send_message
from powershame import api_views
from powershame.mail_jobs import session_rendered_email

from boto.s3.connection import S3Connection

import string
import random

conn = S3Connection( app.config['VIEWER_KEY'], app.config['VIEWER_SECRET'] )

def render( session ):
    secret = ''.join(random.choice(string.ascii_letters) for x in xrange(64))
    bucket = app.config['VID_BUCKET']
    key = '%d.mkv'%session.id
    db.session.add( session )
    session.secret = secret
    session.key = key
    session.bucket = bucket
    db.session.commit()
    start = session.start
    end = (session.end or session.start+6000)
    user = session.user
    callback_url = api.url_for( api_views.v0_1.RenderApi, id=session.id, _external=True, _scheme='https')
    shots = Screenshot.query.filter( Screenshot.user==user, Screenshot.time >= start, Screenshot.time <= end ).all()
    session_data = {
            'id': session.id,
            'height': session.height,
            'width': session.width,
            'shots': [s.render_serialize() for s in shots],
            'bucket': session.bucket,
            'video_key': session.key,
            'callback_url': callback_url,
            'secret': secret }
    send_message( session_data, app.config['RENDERING_QUEUE'] )

def post_render( session_id ):
    session = Session.query.get( session_id )
    db.session.add( session )
    session.rendered = True
    user = User.query.get( session.user )
    for shamer in user.shamers:
        s_view = SessionView( 
                shamer_id=shamer.id, 
                session_id=session.id, 
                secret=''.join( random.choice(string.ascii_lowercase) for x in xrange(64) )
        )
        db.session.add(s_view)
    db.session.commit()
    session_rendered_email( session )

def temp_vid_url( session ):
    url = conn.generate_url(3600, 
            'GET', 
            bucket=app.config['VID_BUCKET'], 
            key= '%d.mkv'%session.id ) 
    return url
