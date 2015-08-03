import config
import urlparse
from app import db
from flask.json import jsonify
from models import Project, Users, AuthInfo
from requests_oauthlib import OAuth1Session
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, redirect, flash, session, url_for


get_oauth_twitter = Blueprint('get_oauth_twitter', __name__, template_folder='templates')


twitter_consumer_key = config.TWITTER_CONSUMER_KEY
twitter_consumer_secret = config.TWITTER_CONSUMER_SECRET


base_url = 'https://api.twitter.com/1/'
request_token_url = 'https://twitter.com/oauth/request_token'
access_token_url = 'https://twitter.com/oauth/access_token'
authorize_url = 'https://api.twitter.com/oauth/authenticate'
consumer_key = twitter_consumer_key,
consumer_secret = twitter_consumer_secret


@get_oauth_twitter.route('/<int:pid>/twitter/oauth', methods=['GET'])
@login_required
def request_token(pid):

    callback_uri = 'http://localhost:5000/{0}/twitter/callback'.format(pid)
    twitter = OAuth1Session(
                            client_key=twitter_consumer_key,
                            client_secret=twitter_consumer_secret,
                            callback_uri=callback_uri
                            )

    twitter.fetch_request_token(request_token_url)

    return redirect(twitter.authorization_url(authorize_url))


@get_oauth_twitter.route('/<int:pid>/twitter/callback', methods=['GET'])
@login_required
def callback(pid):

    callback_uri = 'http://localhost:5000/{0}/twitter/callback'.format(pid)
    twitter = OAuth1Session(
                            client_key=twitter_consumer_key,
                            client_secret=twitter_consumer_secret,
                            callback_uri=callback_uri
                            )

    # return full url
    response_url = request.url

    # parse returned url
    twitter.parse_authorization_response(response_url)

    auth_resp = dict(twitter.fetch_access_token(access_token_url))

    # prevent duplicates from being stored by checking and deleting
    check_auth = AuthInfo.query.filter_by(project_name=pid, api_name='Twitter').first()
    if check_auth is None:
        auth_info = AuthInfo(
                             api_name='Twitter',
                             oauth_token=auth_resp['oauth_token'],
                             oauth_token_secret=auth_resp['oauth_token_secret'],
                             project_name=pid
                             )
    else:
        # delete auth info if it already exists for this API
        AuthInfo.query.filter_by(project_name=pid).delete()
        auth_info = AuthInfo(
                             api_name='Twitter',
                             oauth_token=auth_resp['oauth_token'],
                             oauth_token_secret=auth_resp['oauth_token_secret'],
                             project_name=pid
                             )
    try:
        db.session.add(auth_info)
        db.session.commit()
        flash('Authentication info saved')
        return redirect(url_for('build_timeline_query.main', pid=pid))
    except:
        flash('An Error has occured')
        return redirect('/')  
