import models
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *
from flask.ext.mongoengine.wtf.orm import validators


user_form = model_form(models.User, exclude=['password'])
project_form = model_form(models.Project, exclude=['database', 'created_by'])


# signup form created from user_form
class SignupForm(user_form):
    password = PasswordField('Password', validators=[
                             validators.Required(),
                             validators.EqualTo('confirm', message='Passwords must match')
                             ]
                        )
    confirm = PasswordField('Repeat Password')


# login form will provide a password field (WTForm form field)
class LoginForm(user_form):
    password = PasswordField('Password', validators=[
                             validators.Required()
                             ]
                        )

class ProjectForm(project_form):
    name = TextField('Project Name', valdiators=[
                     validators.Required()
                     ]
                )

