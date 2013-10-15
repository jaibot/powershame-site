from powershame import app
from powershame.urls import Urls
from powershame.httpcodes import HTTPCode
from powershame.models.session import Session
from flask import request, abort

@app.route( Urls.render_notification, methods=['GET','POST'] )
def render_notification():
    if not app.config['BACKEND_AUTH_HEADER'] in request.headers:
        return 'Missing auth token', HTTPCode.denied
    elif not request.headers[ app.config['BACKEND_AUTH_HEADER'] ]==app.config['RENDERER_BACKEND_TOKEN']:
        return 'Incorrect token for renderer', HTTPCode.denied
    else:
        session_id = request.json['session_id']
        vid_url = request.json['vid_url']
        session = Session.query.get( session_id )
        session.vid_url = vid_url
        db.session.commit()
        session.post_render()
