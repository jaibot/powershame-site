from powershame import app, db
from powershame.models.user import User
from powershame.models.session import Session
from powershame.models.session_views import SessionView
from powershame.models.screenshots import Screenshot
from powershame.messaging import send_message

from boto.s3.connection import S3Connection

import string
import random

conn = S3Connection( app.config['VIEWER_KEY'], app.config['VIEWER_SECRET'] )

def render( session ):
    start = session.start
    end = session.end
    user = session.user
    shots = Screenshot.query.filter( Screenshot.user==user, Screenshot.time >= start, Screenshot.time <= end ).all()
    session_data = {
            'id': session.id,
            'shots': [s.render_serialize() for s in shots],
            'video_key': '%d.mkv'%session.id,
            'callback_url': callback_url }
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

def temp_vid_url( session ):
    url = conn.generate_url(3600, 
            'GET', 
            bucket=app.config['VID_BUCKET'], 
            key= '%d.mkv'%session.id ) 
    return url
