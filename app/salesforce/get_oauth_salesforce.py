import config
from app import db
from models import AuthInfo
from requests_oauthlib import OAuth2Session
from flask.ext.login import login_required
from flask import Blueprint, request, redirect, flash, session, url_for


get_oauth_salesforce = Blueprint('get_oauth_salesforce', __name__, template_folder='templates')