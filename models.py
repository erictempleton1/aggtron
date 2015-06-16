import datetime
from flask import url_for
from aggtron import db


class User(db.Document):
    email = db.EmailField(unique=True)
    password = db.StringField(default=True)
    active = db.BooleanField(default=True)
    isAdmin = db.BooleanField(default=False)
    timestamp = db.DateTimeField(default=datetime.datetime.now())


class Project(db.Document):
    Name = db.StringField(default=True)
    Database = db.StringField(default=True)
    Created = db.DateTimeField(default=datetime.datetime.now())
    Created_by = db.StringField(default=True)
    Auth = db.EmbeddedDocumentField(AuthPass, default=AuthPass)


class AuthPass(db.EmbdeddedDocument):
    Username = db.StringField(default=True)
    Password = db.StringField(default=True)