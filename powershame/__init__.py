from flask import Flask, render_template
from flask_mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.restful import Api
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
#app.config.from_object('config')
app.config.from_envvar('POWERSHAME_CONFIG')

handler = RotatingFileHandler('powershame.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.logger.debug('hello')

db = SQLAlchemy(app)
migrate = Migrate( app, db )
manager = Manager(app)
manager.add_command('db', MigrateCommand)

api = Api(app)

mail = Mail( app )

login_manager = LoginManager()
login_manager.init_app(app)

from powershame import views, models
from powershame.api_views import *
