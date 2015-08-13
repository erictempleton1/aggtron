import config
import requests
from app import db
from forms import InstagramUserInfo, InstagramUserFeed
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Users, Project, AuthInfo, InstagramUserFeedQuery, InstagramUserTimelineQuery


build_query = Blueprint('build_query', __name__, template_folder='templates')

@build_query.route('/<int:pid>/instagram/queries', methods=['GET'])
@login_required
def main(pid):
    """ main page for instagram queries """
    # get the current project, and confirm API type
    project = Project.query.filter_by(id=pid,
                                      created_by=current_user.id,
                                      api_type='Instagram'
                                      ).first_or_404()

    proj_auth = AuthInfo.query.filter_by(project_name=project.id).first()

    # placeholder for query to get all instagram queries
    # need to add model

    return render_template(
                           'instagram/user_feed.html',
                           project=project,
                           proj_auth=proj_auth
                           )

@build_query.route('/<int:pid>/instagram/user-query', methods=['GET', 'POST'])
def build_user_query(pid):
    form = InstagramUserInfo()
    if form.validate_on_submit():
        query_title = request.form['query_name']

        # add code for db save here

        flash('Instagram user info query created')
        return redirect(url_for('build_query.main', pid=pid))
    return render_template('instagram/user_info_query.html', form=form)

@build_query.route('/<int:pid>/instagram/feed-query', methods=['GET','POST'])
def build_feed_query(pid):
    form = InstagramUserFeed()
    if form.validate_on_submit():
        query_title = request.form['query_name']

        # add code for db save here

        flash('Instagram user feed query created')
        return redirect(url_for('build_query.main', pid=pid))    
    return render_template('instagram/user_feed_query.html', form=form)