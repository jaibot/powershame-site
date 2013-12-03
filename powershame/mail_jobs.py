from powershame import app, mail
from flask.ext.mail import Message

def registration_email( user ):
    msg = Message("Welcome to Powershame!",
            sender="welcome@powershame.com",
            recipients=[user.email] )
    mail.send( msg )

def session_started_email( session ):
    user = session.owner
    msg = Message("%s has begun a Powershame session"%user.email,
            sender="notification@powershame.com",
            recipients=[shamer.email for shamer in user.shamers] )
    mail.send( msg )

def session_rendered_email( session ):
    user = session.owner
    msg = Message("Check out %s\'s finished Powershame session"%user.email,
            sender="notification@powershame.com",
            recipients=[shamer.email for shamer in user.shamers] )
    mail.send( msg )

