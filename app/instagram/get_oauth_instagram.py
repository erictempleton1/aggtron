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


@get_oauth_instagram.route('/<int:pid>/instagram/oauth', methods=['GET'])
@login_required
def request_token(pid):

    redirect_uri = 'http://localhost:5000/instagram/oauth/callback?pid={0}'.format(pid)
    base_url = 'https://api.instagram.com/oauth/authorize/'

    params = {
                'client_id': instagram_client_id,
                'redirect_uri': redirect_uri,
                'response_type': 'code'
            }
    insta_url = requests.get(base_url, params)          

    return redirect(insta_url.url)

# example response url -
# http://localhost:5000/instagram/oauth/callback?pid=1&code=1b5c96d1fdac407290a3d3eb11f56dea

# not working correctly
@get_oauth_instagram.route('/instagram/oauth/callback?pid=<int:pid>&code=<code>', methods=['GET'])
@login_required
def callback(pid, code):
    
    redirect_uri = 'http://localhost:5000/instagram/oauth/callback?pid={0}'.format(pid)
    request_token_uri = 'https://api.instagram.com/oauth/access_token'
    params = {
                'client_id': instagram_client_id,
                'client_secret': instagram_client_secret,
                'grant_type': authorization_code,
                'redirect_uri': redirect_uri,
                'code': code
            }

    insta_url = requests.post(request_token_uri, params)
    return insta_url.url       