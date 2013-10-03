from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import boto.ses

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# move these to private config TODO
ses_conn = boto.ses.connect_to_region( 
        app.config['SES_REGION'],
        aws_access_key_id = app.config['SES_KEY'],
        aws_secret_access_key = app.config['SES_SECRET'] )

from powershame import views, api, models
