from flask import render_template, redirect, request, abort,  flash
from flask.ext.login import login_user

from app import app
from app import db

from app.models.user import User, get_user_by_login, UsernameExists

from forms import LoginForm, SignupForm

import requests
from werkzeug.datastructures import MultiDict

@app.route('/')
def index():
    return render_template('index.html',user='jai')

@app.route('/login', methods = ['GET','POST'] )
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = get_user_by_login( username, password )
        if not user:
            flash('Sorry - username and/or password incorrect')
        else:
            login( user, request )
        return redirect(request.args.get('next') or '/')
    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/signup', methods = ['GET','POST'] )
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email    = form.email.data
        try:
            user = User( username, password, email )
        except UsernameExists:
            flash('Sorry, someone already has that username!')
        else:
            login( user, request )
    else:
        flash('form did not validate')
    return render_template('signup.html', form = form)

def login( user, request ):
    success = login_user( user )
    if success:
        flash('Logged in successfully!')
    else:
        flash('Something went wrong with login...')

#@app.route('/send_message.html')
#def mail_test():
#    a = requests.post(
#        "https://api.mailgun.net/v2/powershame.mailgun.org/messages",
#        auth=("api", 'key-231mtboe2i9bwkxgw5pses5u-rw6u-j4' ),
#        data={"from": 'jai@powershame.mailgun.org',
#              "to": 'jai@jaibot.com',
#              "subject": "Powershame ON THE INTERNET",
#              "text": "hey you" }
#    )
#    return str(a)

