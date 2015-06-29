import os, datetime
from flask import Blueprint, render_template, url_for
from jinja2 import TemplateNotFound


main_site_index = Blueprint('main_site_index', __name__, template_folder='templates')
auth_pages = Blueprint('auth_pages', __name__)


@main_site_index.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')


