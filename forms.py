import models
from wtforms import Form, validators
from wtforms.fields import *



# signup form created from user_form
class SignupForm(Form):
    email = TextField('Email', validators=[
                      validators.Required()
                      ]
                )
    password = PasswordField('Password', validators=[
                             validators.Required(),
                             validators.EqualTo('confirm', message='Passwords must match')
                             ]
                        )
    confirm = PasswordField('Repeat Password')


# login form will provide a password field (WTForm form field)
class LoginForm(Form):
    email = TextField('Email', validators=[
                      validators.Required()
                      ]
                )
    password = PasswordField('Password', validators=[
                             validators.Required()
                             ]
                        )

class ProjectForm(Form):
    name = TextField('Project Name', validators=[
                     validators.Required()
                     ]
                )
