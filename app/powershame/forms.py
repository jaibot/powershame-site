from flask.ext.wtf import Form, TextField, BooleanField, PasswordField
from flask.ext.wtf import Required

class LoginForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class SignupForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])

class ShamerForm(Form):
    email_1 = TextField( 'email' )
    email_2 = TextField( 'email' )
    email_3 = TextField( 'email' )
    email_4 = TextField( 'email' )
    email_5 = TextField( 'email' )
