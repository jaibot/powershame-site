from powershame import app, db
from powershame.models.user import User
import logging
import boto

def get_mail_conn():
    conn = boto.ses.connect_to_region(
            app.config['AWS_REGION'],
            aws_access_key_id = app.config['SES_KEY'],
            aws_secret_access_key=app.config['SES_SECRET'])
    return conn

def notification_email_content( user, url ):
    return "%(username)s has finished their Powershame session.\
            <a href=\"%(url)s\">Check out what they were up to.</a>\
            "% {'username': user.username, 'url':url }

def send_notification_email( session ):
    logging.debug('Preparing notification for session %s'%str(session)')
    user = User.query.get( session.user )
    shamers = user.shamers
    url = session.url
    addresses = [ shamer.identifier for shamer in shamers ]
    user_email = user.contact_info.first().identifier
    addresses.append( user_email )
    content = notification_email_content( user, url )
    conn = get_mail_conn()
    conn.send_email(
        app.config['NOTIFY_EMAIL_ADDRESS'],
        'Check out what %s was up to' % user.username,
        content,
        addresses )
    logging.debug('sent email')
