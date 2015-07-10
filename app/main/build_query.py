import config
import requests
from requests_oauthlib import OAuth1
from models import Users, Project, AuthInfo
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, flash, redirect


build_query = Blueprint('build_query', __name__, template_folder='templates')

# TODO pass arguments to url
@build_query.route('/<int:pid>/queries')
@login_required
def main(pid):
    project = Project.query.filter_by(id=pid, created_by=current_user.id).first_or_404()
    proj_auth = AuthInfo.query.filter_by(project_name=project.id).first()

    consumer_key = config.TWITTER_CONSUMER_KEY
    consumer_secret = config.TWITTER_CONSUMER_SECRET
    oauth_token = proj_auth.oauth_token
    oauth_token_secret = proj_auth.oauth_token_secret
    url = u'https://api.twitter.com/1.1/statuses/user_timeline.json'

    query = OAuth1(
                   consumer_key,
                   consumer_secret,
                   oauth_token,
                   oauth_token_secret,
                )
    try:
        r = requests.get(url=url, auth=query)
        basic_query = r.json()[1]['text']
    except:
        basic_query = 'An error has occured'    

    return render_template(
                           'main/build_query.html',
                           project=project,
                           proj_auth=proj_auth,
                           basic_query=basic_query
                           )
          