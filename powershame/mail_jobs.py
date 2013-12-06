from flask import url_for
from powershame import app, mail
from powershame.urls import Urls
from powershame.models.session_views import SessionView
from flask.ext.mail import Message

def registration_email( user ):
    msg = Message("Welcome to Powershame!",
            sender="welcome@powershame.com",
            recipients=[user.email] )
    mail.send( msg )

def session_started_email( session ):
    user = session.owner
    for shamer in user.shamers:
        msg = Message("%s has begun a Powershame session"%user.email,
                sender="notification@powershame.com",
                recipients=[shamer.email] )
        mail.send( msg )

def session_rendered_email( session ):
    user = session.owner
    for shamer in user.shamers:
        session_view = SessionView.query.filter_by( session=session, shamer=shamer ).first()
        session_url = url_for('.session_view_shamers', session_secret=session_view.secret, _external=True)
        msg = Message("Check out %s\'s finished Powershame session"%user.email,
                html="<a href=\"%s\">Check out %s\'s finished Powershame session</a>"%(session_url,user.email),
                sender="notification@powershame.com",
                recipients=[shamer.email] )
        mail.send( msg )

