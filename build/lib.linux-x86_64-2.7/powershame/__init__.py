from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
#app.config.from_object('config')
app.config.from_envvar('POWERSHAME_CONFIG')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

import logging
ch = logging.FileHandler( app.config['LOG_FILE'] )
ch.setLevel(logging.DEBUG)
app.logger.addHandler(ch)

from powershame import views, api, models, backend_views
