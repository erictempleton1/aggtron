import models
from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import *


class SignupForm(Form):
    email = TextField('Email', validators=[validators.Required()])
    password = PasswordField('Password', validators=[validators.Required(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    email = TextField('Email', validators=[validators.Required()])
    password = PasswordField('Password', validators=[validators.Required()])


class ProjectForm(Form):
    name = TextField('Project Name', validators=[validators.Required()])
    api_type = SelectField(u'Select API', choices=[
                           ('Twitter', 'Twitter'),
                           ('Instagram', 'Instagram'),
                           ('Google Analytics', 'Google Analytics'),
                           ('Github', 'Github')
                           ])


class TwitterUserTimeline(Form):
    query_name = TextField('Query Name', validators=[validators.Required()])
    include_rts = BooleanField('Include RTs')


class TwitterMentionsTimeline(Form):
    query_name = TextField('Query Name', validators=[validators.Required()])    

    
class InstagramUserInfo(Form):
    query_name = TextField('Query Name', validators=[validators.Required()])


class InstagramUserFeed(Form):
    query_name = TextField('Query Name', validators=[validators.Required()])    