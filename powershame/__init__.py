from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
#app.config.from_object('config')
app.config.from_envvar('POWERSHAME_CONFIG')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from powershame import views, api, models
