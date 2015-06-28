import datetime
from flask import url_for
from aggtron import db


class Users(db.Model):

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    projects = db.relationship('Project', backref='users',
                               lazy='dynamic')

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
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def _init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        return '<Project Name: {0}>'.format(self.name)