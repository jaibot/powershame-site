from powershame import app
from powershame.messaging import send_message
from powershame.models.session import Session
from powershame.models.screenshots import Screenshot

session = Session.query.get( 84 )
shots = Screenshot.query.filter( Screenshot.user==session.user, Screenshot.time >= session.start, Screenshot.time <= session.end ).all()

session_data = {
        'id': session.id,
        'shots': [s.render_serialize() for s in shots],
        'video_key': '%d.mkv'%session.id,
}
send_message( session_data, app.config['RENDERING_QUEUE'] )
