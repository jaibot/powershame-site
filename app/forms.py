from flask.ext.wtf import Form, TextField, BooleanField
from flask.ext.wtf import Required

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = TextField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class SignupForm(Form):
    username = TextField('username', validators = [Required()])
    password = TextField('password', validators = [Required()])
