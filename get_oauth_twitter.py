import config
from aggtron import db
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
callback_uri = 'http://www.example.com/oauth'
consumer_key = twitter_consumer_key,
consumer_secret = twitter_consumer_secret


@get_oauth_twitter.route('/twitter/oauth', methods=['GET'])
@login_required
def demo():
    twitter = OAuth1Session(
                            client_key=twitter_consumer_key,
                            client_secret=twitter_consumer_secret,
                            callback_uri=callback_uri
                            )

    token = twitter.fetch_request_token(request_token_url)

    return jsonify(token)



