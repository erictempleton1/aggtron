import config
import urlparse
import requests
from app import db
from flask.json import jsonify
from models import Project, Users, AuthInfo
from requests_oauthlib import OAuth2Session
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, redirect, flash, session, url_for


get_oauth_instagram = Blueprint('get_oauth_instagram', __name__, template_folder='templates')


instagram_client_id = config.INSTAGRAM_CLIENT_ID
instagram_client_secret = config.INSTAGRAM_CLIENT_SECRET
authorize_url = 'https://api.instagram.com/oauth/authorize/'



@get_oauth_instagram.route('/<int:pid>/instagram/oauth', methods=['GET'])
@login_required
def request_token(pid):

    redirect_uri = 'http://localhost:5000/instagram/oauth/callback?pid={0}'.format(pid)
    oauth = OAuth2Session(client_id=instagram_client_id, redirect_uri=redirect_uri)
    authorization_url, state = oauth.authorization_url(authorize_url)

    session['oauth_state'] = state

    return redirect(authorization_url)

# example response url -
# http://localhost:5000/instagram/oauth/callback?pid=1&code=1b5c96d1fdac407290a3d3eb11f56dea

@get_oauth_instagram.route('/instagram/oauth/callback', methods=['GET'])
@login_required
def callback():
    code = request.args.get('code')
    return code
        