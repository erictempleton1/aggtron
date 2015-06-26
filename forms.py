import models
from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import *


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
