import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound


main_site_index = Blueprint('main_site_index', __name__, template_folder='templates')
auth_pages = Blueprint('auth_pages', __name__)


@main_site_index.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')


# todo - fix logged in check in template