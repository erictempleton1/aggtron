import os, datetime
from flask import Blueprint, render_template, url_for
from flask.ext.login import login_required


add_project = Blueprint('add_project', __name__, template_folder='templates')


@add_project.route('/create', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('api_auth.html')

# todo - fix template inheritence & add forms