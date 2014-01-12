from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, FieldList
from flask.ext.wtf import Required

class LoginForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class SignupForm(Form):
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])


class ShamerForm( Form ):
    shamers = FieldList( TextField('email') )

