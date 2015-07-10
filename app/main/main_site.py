import os, datetime
from models import Users, Project
from flask import Blueprint, render_template, url_for
from flask.ext.login import current_user
from jinja2 import TemplateNotFound


main_site_index = Blueprint('main_site_index', __name__, template_folder='templates')
auth_pages = Blueprint('auth_pages', __name__)


@main_site_index.route('/', methods=['GET', 'POST'])
def index():
    # list projects or no projects for user
    if current_user.is_authenticated():
        projects = Project.query.filter_by(created_by=current_user.id)
    else:
        projects = 'No projects created'    
    return render_template('main/index.html', projects=projects)


