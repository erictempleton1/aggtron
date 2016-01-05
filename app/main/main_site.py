import random
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
    x1 = random.sample(range(1, 50), 20)
    y1 = random.sample(range(1, 50), 20)

    # select the tools we want
    TOOLS="pan,wheel_zoom,box_zoom,reset,save"

    # the red and blue graphs will share this data range
    xr1 = Range1d(start=0, end=30)
    yr1 = Range1d(start=0, end=30)

    # build our figures
    p1 = figure(
            x_range=xr1, y_range=yr1, tools=TOOLS,
                plot_width=500, plot_height=300, logo=None,
                toolbar_location=None, outline_line_color=None
    )
    p1.scatter(x1, y1, size=12, color="red", alpha=0.5)

    # hide gridlines
    p1.xgrid.grid_line_color = None
    p1.ygrid.grid_line_color = None

    # remove minor tickmarks
    p1.yaxis[0].ticker.num_minor_ticks = 0
    p1.xaxis[0].ticker.num_minor_ticks = 0

    script, div = components(p1)

    return render_template('main/index.html',
                           projects=projects,
                           script=script,
                           div=div)


