import config
import requests
from app import db
from forms import InstagramUserInfo, InstagramUserFeed
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Users, Project, AuthInfo, InstagramUserFeedQuery, InstagramUserInfoQuery


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

    # load authorization info for given project
    proj_auth = AuthInfo.query.filter_by(project_name=project.id).first()

    # return all user info queries for template
    user_info_queries = InstagramUserInfoQuery.query.filter_by(
                                                          project_name=project.id,
                                                          created_by=current_user.id
                                                          )

    # return all user feed queries for template
    user_feed_queries = InstagramUserFeedQuery.query.filter_by(
                                                               project_name=project.id,
                                                               created_by=current_user.id
                                                               )

    # placeholder for basic query to Instagram API
    if proj_auth:
        feed_url = 'https://api.instagram.com/v1/users/self/media/recent/'

        params = {
                    'access_token': proj_auth.oauth_token,
                    'count': 1
                }   
    else:
        proj_auth = False

    try:
        r = requests.get(feed_url, params=params)
        basic_query = r.json()
    except:
        basic_query = 'Error: unable to complete request'        


    return render_template(
                           'instagram/user_feed.html',
                           project=project,
                           proj_auth=proj_auth,
                           basic_query=basic_query,
                           user_info_queries=user_info_queries,
                           user_feed_queries=user_feed_queries
                           )

@build_query.route('/<int:pid>/instagram/user-query', methods=['GET', 'POST'])
@login_required
def build_user_query(pid):
    """ form to create a new user info query """
    # get the current project, and confirm API type
    project = Project.query.filter_by(id=pid,
                                      created_by=current_user.id,
                                      api_type='Instagram'
                                      ).first_or_404()

    # load authorization info for given project
    proj_auth = AuthInfo.query.filter_by(project_name=project.id).first()

    form = InstagramUserInfo()
    if form.validate_on_submit():
        query_title = request.form['query_name']

        new_query = InstagramUserInfoQuery(
                                           auth_id=proj_auth.id,
                                           name=query_title,
                                           created_by=current_user.id,
                                           project_name=pid
                                           )
        try:
            db.session.add(new_query)
            db.session.commit()
            flash('Instagram user info query created')
            return redirect(url_for('build_query.main', pid=pid))
        except:
            flash('An error occured')
            return redirect(url_for('build_query.main', pid=pid))

    return render_template('instagram/user_info_query.html', form=form)

@build_query.route('/<int:pid>/instagram/feed-query', methods=['GET','POST'])
@login_required
def build_feed_query(pid):
    """ form to created a new user feed query """
    # get the current project, and confirm API type
    project = Project.query.filter_by(id=pid,
                                      created_by=current_user.id,
                                      api_type='Instagram'
                                      ).first_or_404()

    # load authorization info for given project
    proj_auth = AuthInfo.query.filter_by(project_name=project.id).first()

    form = InstagramUserFeed()
    if form.validate_on_submit():
        query_title = request.form['query_name']

        new_query = InstagramUserFeedQuery(
                                           auth_id=proj_auth.id,
                                           name=query_title,
                                           created_by=current_user.id,
                                           project_name=pid
                                           )
        try:
            db.session.add(new_query)
            db.session.commit()
            flash('Instagram user feed query created')
            return redirect(url_for('build_query.main', pid=pid))
        except:
            flash('An error occured')
            return redirect(url_for('build_query.main', pid=pid))

    return render_template('instagram/user_feed_query.html', form=form)

@build_query.route('/<int:pid>/<int:qid>/query-status-info', methods=['GET'])
@login_required
def change_status_info(qid, pid):
    """ check to see if user info query is enabled or disabled """
    existing_query = InstagramUserInfoQuery.query.filter_by(
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

    return redirect(url_for('build_query.main', pid=pid)) 

@build_query.route('/<int:pid>/<int:qid>/query-status-feed', methods=['GET'])
@login_required
def change_status_feed(qid, pid):
    """ check to see if user feed query is enabled or disabled """
    existing_query = InstagramUserFeedQuery.query.filter_by(
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
            flash('Query disabled')
    except:
        flash('An error occured')

    return redirect(url_for('build_query.main', pid=pid))



""" still in dev. will work on later """    

@build_query.route('/<int:pid>/<int:qid>/delete-user-query', methods=['GET'])
@login_required
def remove_user_query(qid, pid):
    """ delete specific user info query """
    try:
        user_query = InstagramUserInfoQuery.query.filter_by(
                                               id=qid,
                                               created_by=current_user.id
                                               )
        db.session.delete(user_query)
        db.session.commit()
        flash('Query deleted')
    except:
        flash('An error occured. Unable to delete query')

    return redirect(url_for('build_query.main', pid=pid))

@build_query.route('/<int:pid>/<int:qid>/delete-feed-query', methods=['GET'])
@login_required
def remove_feed_query(qid, pid):
    """ delete specific user feed query """
    try:
        feed_query = InstagramUserFeedQuery.query.filter_by(
                                                            id=qid,
                                                            created_by=current_user.id
                                                            ).first()
        db.session.delete(feed_query)
        db.session.commit()
    except:
        flash('An error occured')    

    return redirect(url_for('build_query.main', pid=pid))  
    
# delete url is not deleting queries
