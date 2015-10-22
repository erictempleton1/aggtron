import datetime
from flask import url_for
from app import db


class Users(db.Model):

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    projects = db.relationship('Project', backref='users',
                               lazy='joined')


    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Email: {0}>'.format(self.email)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Project(db.Model):

    __tablename__ = 'project'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    api_type = db.Column(db.String(120))
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    authinfo = db.relationship('AuthInfo', backref='project', lazy='dynamic')
    twitter_timeline_query = db.relationship('TwitterUserTimelineQuery', backref='project', lazy='dynamic')
    twitter_mentions_query = db.relationship('TwitterMentionsTimelineQuery', backref='project', lazy='dynamic')


    def __init__(self, name, api_type, created_by):
        self.name = name
        self.api_type = api_type
        self.created_by = created_by

    def __repr__(self):
        return '<Project Name: {0}>'.format(self.name)


class AuthInfo(db.Model):

    __tablename__ = 'authinfo'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String())
    oauth_token = db.Column(db.String())
    oauth_token_secret = db.Column(db.String())
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    project_name = db.Column(db.Integer, db.ForeignKey('project.id'))


    def __init__(self, api_name, oauth_token, oauth_token_secret, project_name):
        self.api_name = api_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.project_name = project_name

    def __repr__(self):
        return '<OAuth Token: {0}>'.format(self.oauth_token)


class TwitterUserTimelineQuery(db.Model):

    __tablename__ = 'twitterusertimelinequery'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.Integer)
    name = db.Column(db.String())
    query_type = db.Column(db.String(), default='twitter user timeline')
    include_rts = db.Column(db.String())
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=True)
    last_run = db.Column(db.DateTime, default=None)
    project_name = db.Column(db.Integer, db.ForeignKey('project.id'))


    def __init__(self, auth_id, name, include_rts, created_by, project_name):
        self.auth_id = auth_id
        self.name = name
        self.include_rts = include_rts
        self.created_by = created_by
        self.project_name = project_name

    def __repr__(self):
        return '<Query Name: {0}>'.format(self.name)

class TwitterUserInfoQuery(db.Model):

    __tablename__ = 'twitteruserinfoquery'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.Integer)
    name = db.Column(db.String())
    query_type = db.Column(db.String(), default='twitter user info')
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=True)
    last_run = db.Column(db.DateTime, default=True)
    project_name = db.Column(db.Integer, db.ForeignKey('project.id'))


    def __init__(self, auth_id, name, created_by, project_name):
        self.auth_id = auth_id
        self.name = name
        self.created_by = created_by
        self.project_name = project_name

    def __repr__(self):
        return '<Query Name {0}>'.format(self.name)         


class TwitterMentionsTimelineQuery(db.Model):

    __tablename__ = 'twittermentionstimelinequery'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.Integer)
    name = db.Column(db.String())
    query_type = db.Column(db.String(), default='twitter mentions timeline')
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=True)
    last_run = db.Column(db.DateTime, default=None)
    project_name = db.Column(db.Integer, db.ForeignKey('project.id'))


    def __init__(self, auth_id, name, created_by, project_name):
        self.auth_id = auth_id
        self.name = name
        self.created_by = created_by
        self.project_name = project_name

    def __repr__(self):
        return '<Query Name {0}>'.format(self.name)       


class InstagramUserFeedQuery(db.Model):
    
    __tablename__ = 'instagramuserfeedquery'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.Integer)
    name = db.Column(db.String())
    query_type = db.Column(db.String(), default='instagram user feed')
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=True)
    last_run = db.Column(db.DateTime, default=None)
    project_name = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, auth_id, name, created_by, project_name):
        self.auth_id = auth_id
        self.name = name
        self.created_by = created_by
        self.project_name = project_name

    def __repr__(self):
        return '<Query Name {0}>'.format(self.name)

class InstagramUserInfoQuery(db.Model):
    
    __tablename__ = 'instagramuserinfoquery'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.Integer)
    name = db.Column(db.String())
    query_type = db.Column(db.String(), default='instagram user info')
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=True)
    last_run = db.Column(db.DateTime, default=None)
    project_name = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, auth_id, name, created_by, project_name):
        self.auth_id = auth_id
        self.name = name
        self.created_by = created_by
        self.project_name = project_name

    def __repr__(self):
        return '<Query Name {0}>'.format(self.name)
