import config
import requests
from app import db
from models import Users, Project, AuthInfo
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, flash, redirect, url_for


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
    return render_template('instagram/user_feed.html')