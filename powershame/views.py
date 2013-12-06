from flask import render_template, redirect, request, abort,  flash, url_for
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.mail import Message
from time import sleep

from powershame import app, db, jobs
from powershame.urls import Urls
from powershame.strings import Strings
from powershame import db
from powershame.httpcodes import HTTPCode
from powershame.mail_jobs import registration_email

from powershame.models.user import User, get_user_by_login
from powershame.models.session_views import SessionView
from powershame.models.session import Session
from powershame.models.shamers import Shamer

from forms import LoginForm, SignupForm, ShamerForm

@app.route('/qwerasdf')
def testjai():
    jobs.render( Session.query.first() )
    return 'yay',200

@app.route('/')
def index():
    return standard_render('index.html')

@app.route(Urls.logout)
def logout():
    logout_user()
    return standard_render('index.html')

@app.route(Urls.login, methods = ['GET','POST'] )
def login_view():
    if current_user.is_authenticated():
        return redirect( '/' )
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = get_user_by_login( email, password )
        if not user:
            flash("Hmmm, that's not quite right.")
            return standard_render('login.html', 
                title = 'Sign In',
                form = form )
        else:
            login( user )
            sleep(0.5) #TODO for some reason login takes a bit to register? without this, might not be logged in when page registers
            return redirect(request.args.get('next') or '/')
    return standard_render('login.html', 
        title = 'Sign In',
        form = form )

@app.route(Urls.signup, methods = ['GET','POST'] )
def signup():
    if current_user:
        return redirect( '/' )
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user, reason = create_user_or_not( **form.data )
            if user:
                db.session.add(user)
                db.session.commit()
                flash('You joined Powershame!')
                login( user )
            else:
                flash("There was a problem creating your account: %s" % reason )
        else:
            flash('Er, something went wrong with signup - could you try again?')
    return standard_render('signup.html', form = form )

@app.route( Urls.shamers, methods=['GET','POST'] )
@login_required
def shamers():
    form = ShamerForm()
    if form.validate_on_submit():
        current_shamers = current_user.shamers.all()
        current_shamer_emails = [x.email for x in current_shamers]
        new_emails = set([ x.data for x in ( form.email_1, form.email_2, form.email_3, form.email_4, form.email_5 ) ])
        for new_email in new_emails:
            if new_email and not new_email in current_shamer_emails:
                shamer = Shamer( user=current_user.id, email=new_email )
                db.session.add(shamer)
        for old_email in current_shamer_emails:
            if not old_email in new_emails:
                shamer_to_delete = Shamer.query.filter_by( email=old_email, user=current_user.id ).first()
                db.session.delete( shamer_to_delete )
        form = ShamerForm()
    db.session.commit()
    return standard_render( 'shamers.html', form=form, shamers=current_user.shamers.all() )

@app.route( Urls.sessions, methods=['GET'] )
@login_required
def sessions():
    all_sessions = current_user.sessions.all()
    return standard_render( 'sessions.html', sessions=all_sessions )

@app.route( Urls.session_view_shamers+'/<session_secret>', methods=['GET'] )
def session_view_shamers( session_secret ):
    session_view = SessionView.query.filter_by( secret = session_secret ).first()
    session = Session.query.get( session_view.session_id )
    url = jobs.temp_vid_url( session )
    return standard_render( 'session_view.html', session=session, url=url )

@app.route( Urls.session_view+'/<session_id>', methods=['GET'] )
@login_required
def session_view( session_id ):
    session = Session.query.get( session_id )
    if session and session.owner == current_user:
        url = jobs.temp_vid_url( session )
        return standard_render( 'session_view.html', session=session, url=url )
    else:
        abort(401)

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

def create_user_or_not( email, password ):
    """Create user if valid signup values. Return bool-status, reason"""
    if User.query.filter_by( email=email ).first():
        return None, "email already exists"
    user = User( email=email, password=password )
    if user:
        registration_email( user )
        return user, "success"

