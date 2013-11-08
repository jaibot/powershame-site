from flask import render_template, redirect, request, abort,  flash
from flask.ext.login import login_user, logout_user, current_user

from powershame import app, db
from powershame.urls import Urls
from powershame.strings import Strings
from powershame import db
from powershame.httpcodes import HTTPCode
from powershame import jobs

from powershame.models.user import User, get_user_by_login
from powershame.models.session_views import SessionView
from powershame.models.session import Session

from forms import LoginForm, SignupForm, ShamerForm

@app.route('/')
def index():
    return standard_render('index.html')

@app.route(Urls.logout)
def logout():
    logout_user()
    return standard_render('index.html')

@app.route(Urls.login, methods = ['GET','POST'] )
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = get_user_by_login( email, password )
        if not user:
            flash("Hmmm, that's not quite right.")
        else:
            login( user )
        return redirect(request.args.get('next') or '/')
    return standard_render('login.html', 
        title = 'Sign In',
        form = form )

@app.route(Urls.signup, methods = ['GET','POST'] )
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User( **form.data )
        db.session.add(user)
        db.session.commit()
        if user:
            login( user )
    else:
        flash('form did not validate')
    return standard_render('signup.html', form = form )

@app.route( Urls.shamers, methods=['GET','POST'] )
def shamers():
    form = ShamerForm()
    if form.validate_on_submit():
        user.add_shamer( form.email_address )
    return standard_render( 'shamers.html', form=form )

@app.route( Urls.session_view, methods=['GET'] )
def session_view( session_secret ):
    session_view = SessionView.query.filter_by( secret = session_secret ).first()
    session = Session.query.get( session_view.session_id )
    url = jobs.temp_vid_url( session )
    return standard_render( 'session_view.html', session=session, url=url )

def standard_render( template, **kwargs ):
    kwargs['user'] = current_user
    kwargs['strings'] = Strings
    kwargs['urls'] = Urls
    return render_template( template, **kwargs )

def login( user ) :
    if login_user( user ):
        app.logger.debug('%s logged in'%user.email)
        app.logger.debug('current user: %s'% current_user.email )
        flash('Logged in successfully!')
    else:
        flash('Something went wrong with login...')
