import config
import requests
from app import db
from requests_oauthlib import OAuth1
from forms import TwitterUserTimeline
from models import Users, Project, AuthInfo, TwitterUserTimelineQuery
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, flash, redirect, url_for


build_query = Blueprint('build_query', __name__, template_folder='templates')


@build_query.route('/<int:pid>/queries', methods=['GET'])
@login_required
def main(pid):

    project = Project.query.filter_by(id=pid, created_by=current_user.id).first_or_404()
    proj_auth = AuthInfo.query.filter_by(project_name=project.id).first()
    proj_queries = TwitterUserTimelineQuery.query.filter_by(project_name=project.id, created_by=current_user.id)

    if proj_auth:
      # check to make sure auth creds are in the db
      consumer_key = config.TWITTER_CONSUMER_KEY
      consumer_secret = config.TWITTER_CONSUMER_SECRET
      oauth_token = proj_auth.oauth_token
      oauth_token_secret = proj_auth.oauth_token_secret
      url = u'https://api.twitter.com/1.1/statuses/user_timeline.json?count=1'

      query = OAuth1(
                     consumer_key,
                     consumer_secret,
                     oauth_token,
                     oauth_token_secret,
                  )
    else:
        # prompt user to authenticate if no auth creds are found
        proj_auth = False


    try:
        # make a basic query to confirm connection
        r = requests.get(url=url, auth=query)
        basic_query = r.json()[0]['id']
    except:
        basic_query = 'Error: unable to complete request'   

    return render_template(
                           'main/build_query.html',
                           project=project,
                           proj_auth=proj_auth,
                           basic_query=basic_query,
                           proj_queries=proj_queries
                           )


@build_query.route('/<int:pid>/twitter/build-query', methods=['GET', 'POST'])
@login_required
def build(pid):
    form = TwitterUserTimeline()
    if form.validate_on_submit():
        query_title = request.form['query_name']
        include_rts = request.form.get('include_rts')

        new_query = TwitterUserTimelineQuery(
                                             name=query_title,
                                             include_rts=include_rts,
                                             created_by=current_user.id,
                                             project_name=pid
                                             )
        db.session.add(new_query)
        db.session.commit()
        flash('Query Created')
        # placeholder for db save
        return redirect(url_for('build_query.main', pid=pid))

    return render_template('twitter/new_query.html', form=form)    
    
          