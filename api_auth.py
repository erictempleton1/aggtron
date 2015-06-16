import os, datetime
from flask import Blueprint, render_template, url_for
from flask.ext.login import login_required


api_auth = Blueprint('api_auth', __name__, template_folder='templates')


@api_auth.route('/auth', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('api_auth.html')

# todo - fix template inheritence & add forms