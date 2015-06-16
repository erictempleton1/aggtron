import datetime
from flask import url_for
from aggtron import db


class User(db.Document):
    email = db.EmailField(unique=True)
    password = db.StringField(default=True)
    active = db.BooleanField(default=True)
    isAdmin = db.BooleanField(default=False)
    timestamp = db.DateTimeField(default=datetime.datetime.now())


class AuthPass(db.EmbeddedDocument):
    username = db.StringField(default=True)
    password = db.StringField(default=True)


class Project(db.Document):
    name = db.StringField(default=True)
    database = db.StringField(default=True)
    created = db.DateTimeField(default=datetime.datetime.now())
    created_by = db.ReferenceField(User)
    #auth = db.EmbeddedDocumentField(AuthPass, default=AuthPass)