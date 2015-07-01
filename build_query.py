from models import Users, Project
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, flash, redirect


build_query = Blueprint('build_query', __name__, template_folder='templates')

# TODO pass arguments to url
@build_query.route('/<pid>/query')
@login_required
def main():
    return render_template('main/build_query.html')