import os, datetime
from models import Users, Project
from flask import Blueprint, render_template, url_for
from flask.ext.login import current_user
from jinja2 import TemplateNotFound

from bokeh.plotting import figure
from bokeh.models import Range1d
from bokeh.embed import components


main_site_index = Blueprint('main_site_index', __name__, template_folder='templates')
auth_pages = Blueprint('auth_pages', __name__)


@main_site_index.route('/', methods=['GET', 'POST'])
def index():
    # list projects or no projects for user
    if current_user.is_authenticated():
        projects = Project.query.filter_by(created_by=current_user.id)
    else:
        projects = 'No projects created'

    # create some data
    x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]

    # select the tools we want
    TOOLS="pan,wheel_zoom,box_zoom,reset,save"

    # the red and blue graphs will share this data range
    xr1 = Range1d(start=0, end=30)
    yr1 = Range1d(start=0, end=30)

    # build our figures
    p1 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, plot_width=300, plot_height=300)
    p1.scatter(x1, y1, size=12, color="red", alpha=0.5)

    script, div = components(p1)

    return render_template('main/index.html',
                           projects=projects,
                           script=script,
                           div=div)


