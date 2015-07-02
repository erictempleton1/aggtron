from models import Users, Project
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, flash, redirect


build_query = Blueprint('build_query', __name__, template_folder='templates')

# TODO pass arguments to url
@build_query.route('/<int:pid>/queries')
@login_required
def main(pid):
    project = Project.query.filter_by(id=pid, created_by=current_user.id).first_or_404()
    return render_template('main/build_query.html', project=project)
            