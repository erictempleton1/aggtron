import config
import requests
from app import db
from requests_oauthlib import OAuth1
from flask.ext.login import current_user, login_required
from forms import TwitterUserTimeline, TwitterMentionsTimeline
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import (Users, Project, AuthInfo,
                    TwitterUserTimelineQuery,
                    TwitterMentionsTimelineQuery,
                    TwitterUserInfoQuery)


build_timeline_query = Blueprint('build_timeline_query', __name__, template_folder='templates')


@build_timeline_query.route('/<int:pid>/twitter/queries', methods=['GET'])
@login_required
def main(pid):
    """ main page for twitter queries """
    # get the current project, and confirm API type
    project = Project.query.filter_by(id=pid,
                                      created_by=current_user.id,
                                      api_type='Twitter'
                                      ).first_or_404()

    # get the authorization for current project
    proj_auth = AuthInfo.query.filter_by(project_name=project.id).first()

    # return all timeline queries
    timeline_queries = TwitterUserTimelineQuery.query.filter_by(
                                                                project_name=project.id,
                                                                created_by=current_user.id
                                                                )

    # return all mentions queries
    mentions_queries = TwitterMentionsTimelineQuery.query.filter_by(
                                                                    project_name=project.id,
                                                                    created_by=current_user.id
                                                                    )
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
        basic_query = r.json()
    except:
        basic_query = 'Error: unable to complete request'   

    return render_template(
                           'main/build_query.html',
                           project=project,
                           proj_auth=proj_auth,
                           basic_query=basic_query,
                           timeline_queries=timeline_queries,
                           mentions_queries=mentions_queries
                           )

@build_timeline_query.route('/<int:pid>/twitter/info-query', methods=['GET', 'POST'])
@login_required
def build_user_info(pid):
    """ create a new query to save the user's profile info """
    pass    


@build_timeline_query.route('/<int:pid>/twitter/mentions-query', methods=['GET', 'POST'])
@login_required
def build_mentions(pid):
    """ create a new query to save a user's mentions """
      # get the current project, and confirm API type
    project = Project.query.filter_by(id=pid,
                                      created_by=current_user.id,
                                      api_type='Twitter'
                                      ).first_or_404()

    # get the authorization for current project
    proj_auth = AuthInfo.query.filter_by(project_name=project.id).first()

    form = TwitterMentionsTimeline()
    if form.validate_on_submit():
        query_title = request.form['query_name']

        new_query = TwitterMentionsTimelineQuery(
                                                 auth_id=proj_auth.id,
                                                 name=query_title,
                                                 created_by=current_user.id,
                                                 project_name=pid
                                                 )
        try:
            db.session.add(new_query)
            db.session.commit()
            flash('Twitter Mentions Query Created')
            return redirect(url_for('build_timeline_query.main', pid=pid))
        except:
            flash('An error occured')    
            return redirect(url_for('build_timeline_query.main', pid=pid))

    return render_template('twitter/new_mentions_query.html', form=form)    


@build_timeline_query.route('/<int:pid>/twitter/timeline-query', methods=['GET', 'POST'])
@login_required
def build(pid):
    """ create a new query to save a user's timeline """
    # get the current project, and confirm API type
    project = Project.query.filter_by(id=pid,
                                      created_by=current_user.id,
                                      api_type='Twitter'
                                      ).first_or_404()

    # get the authorization for current project
    proj_auth = AuthInfo.query.filter_by(project_name=project.id).first()

    form = TwitterUserTimeline()
    if form.validate_on_submit():
        query_title = request.form['query_name']
        include_rts = request.form.get('include_rts')

        new_query = TwitterUserTimelineQuery(
                                             auth_id=proj_auth.id,
                                             name=query_title,
                                             include_rts=include_rts,
                                             created_by=current_user.id,
                                             project_name=pid
                                             )
        try:
            db.session.add(new_query)
            db.session.commit()
            flash('Twitter Timeline Query Created')
            return redirect(url_for('build_timeline_query.main', pid=pid))
        except:
            flash('An error occured')
            return redirect(url_for('build_timeline_query.main', pid=pid))
    
    return render_template('twitter/new_timeline_query.html', form=form)


@build_timeline_query.route('/<int:pid>/<int:qid>/query-status-timeline', methods=['GET'])
@login_required
def change_status_timeline(qid, pid):
    """ check to see if timeline query is enabled or disabled"""
    existing_query = TwitterUserTimelineQuery.query.filter_by(
                                                          id=qid,
                                                          created_by=current_user.id
                                                          ).first_or_404()
    try:
        # check query status and update
        if existing_query.enabled:
            existing_query.enabled = False
            db.session.commit()
            flash('Query disabled')
        else:
            existing_query.enabled = True
            db.session.commit()
            flash('Query enabled')
    except:
        flash('An error occured')

    return redirect(url_for('build_timeline_query.main', pid=pid))

@build_timeline_query.route('/<int:pid>/<int:qid>/query-status-mentions', methods=['GET'])
@login_required
def change_status_mentions(qid, pid):
    """ check to see if mentions query is enabled or disabled"""
    existing_query = TwitterMentionsTimelineQuery.query.filter_by(
                                                 id=qid,
                                                 created_by=current_user.id).first_or_404()
    try:
        # check query status and update
        if existing_query.enabled:
            existing_query.enabled = False
            db.session.commit()
        else:
            existing_query.enabled = True
            db.session.commit()
    except:
        flash('An error occured')

    return redirect(url_for('build_timeline_query.main', pid=pid))                                                   

# TODO need to add change_status_mentions in template
# TODO rework disable/enable query to apply to all queries?
# TODO add user mentions query pages
# TODO add delete button for queries?
# TODO might need to re-think schema layout