from flask import render_template, redirect, request
from flask.ext.login import LoginManager,login_user
from flask.ext.principal import identity_changed

from app import app
from app import db
from app import login_manager
from models.user import User, load_user, name_exists
from forms import LoginForm, SignupForm

import requests
from werkzeug.datastructures import MultiDict

@app.route('/')
def index():
    return render_template('index.html',user='jai')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    # Validate form input
    if form.validate_on_submit():
        # Retrieve the user from the hypothetical datastore
        user = User.query.filter_by(username=form.username.data).first()
        # Compare passwords (use password hashing production)
        if user.check_pw( form.password.data ) :
            login_user(user)
            return redirect(request.args.get('next') or '/')
        else:
            return redirect('/ohno')
    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    # Validate form input
    if form.validate_on_submit():
        if name_exists( form.username.data ):
            return redirect('/ohno')
        else:
            user=User(form.username.data, form.password.data)
            login_user(user)
            return redirect(request.args.get('next') or '/')
    return render_template('signup.html', 
        title = 'Signup',
        form = form)

@app.route('/send_message.html')
def mail_test():
    a = requests.post(
        "https://api.mailgun.net/v2/powershame.mailgun.org/messages",
        auth=("api", 'key-231mtboe2i9bwkxgw5pses5u-rw6u-j4' ),
        data={"from": 'jai@powershame.mailgun.org',
              "to": 'jai@jaibot.com',
              "subject": "Powershame ON THE INTERNET",
              "text": "hey you" }
    )
    return str(a)
