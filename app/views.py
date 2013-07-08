from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Jai' } # fake user
    return render_template("index.html",
      title = 'Home',
      user = user) 

@app.route('/channel.html')
def fb_channel():
    return render_template("channel.html")
