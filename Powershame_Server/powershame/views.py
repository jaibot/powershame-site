from flask import render_template, redirect, request, abort,  flash
from flask.ext.login import login_user, logout_user, current_user

from powershame import app
from powershame import db
from powershame import ses_conn

from powershame.models.user import User, get_user_by_login, UsernameExists

from forms import LoginForm, SignupForm, ShamerForm

import requests
from werkzeug.datastructures import MultiDict

@app.route('/')
def index():
    return standard_render('index.html')

@app.route('/logout')
def logout():
    logout_user()
    return standard_render('index.html')

#TODO: I am doing too many things here; refactor
@app.route('/login', methods = ['GET','POST'] )
def login():
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
    return standard_render('login.html', 
        title = 'Sign In',
        form = form )

@app.route('/signup', methods = ['GET','POST'] )
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email    = form.email.data
        try:
            user = User( username, password, email )
            ses_conn.send_email( 'jai@powershame.com',
                    'Welcome to Powershame!',
                    'Welcome to Powershame!',
                    email)
        except UsernameExists:
            flash('Sorry, someone already has that username!')
        else:
            login( user, request )
    else:
        flash('form did not validate')
    return standard_render('signup.html', form = form )

@app.route( app.config['URLS']['sessions'],methods = ['GET','POST'] )
def list_sessions():
    return standard_render( 'list_sessions.html' )

@app.route( app.config['URLS']['shamers'], methods=['GET','POST'] )
def shamers():
    form = ShamerForm()
    if form.validate_on_submit():
        user.add_shamer( form.email_address )
    return standard_render( 'shamers.html', form=form )


def standard_render( template, **kwargs ):
    kwargs['user'] = current_user
    kwargs['strings'] = app.config['STRINGS']
    kwargs['urls'] = app.config['URLS']
    return render_template( template, **kwargs )

def login( user, request ):
    success = login_user( user )
    if success:
        flash('Logged in successfully!')
    else:
        flash('Something went wrong with login...')

#def add_shamer( user, email ):
