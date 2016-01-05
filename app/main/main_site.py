import random
import os, datetime
from collections import OrderedDict

from models import Users, Project
from flask import Blueprint, render_template, url_for
from flask.ext.login import current_user
from jinja2 import TemplateNotFound

from bokeh.plotting import figure
from bokeh.models import Range1d, HoverTool
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
    x1 = [0, 1, 2, 3, 4, 5, 6, 7]
    y1 = [0, 6, 7, 2, 4, 5, 5, 5]

    x2 = [0, 1, 2, 3, 4, 5, 6, 7]
    y2 = [0, 7, 6, 4, 2, 5, 2, 3]

    x3 = [0, 1, 2, 3, 4, 5, 6, 7]
    y3 = [0, 2, 5, 2, 6, 2, 4, 2]

    # select the tools we want
    TOOLS = 'pan,wheel_zoom,box_zoom,reset,save,hover'

    # the red and blue graphs will share this data range
    xr1 = Range1d(start=0, end=7)
    yr1 = Range1d(start=0, end=7)

    # build our figures
    p1 = figure(
                x_range=xr1, y_range=yr1, tools=TOOLS,
                plot_width=400, plot_height=400, logo=None,
                outline_line_color=None
    )

    # build multi line and set options
    p1.multi_line(
            [x1, x2, x3],
            [y1, y2, y3],
            color=['red', 'blue', 'green'],
            line_width=2
    )

    # hide gridlines
    p1.xgrid.grid_line_color = None
    p1.ygrid.grid_line_color = None

    # remove minor tickmarks
    p1.yaxis[0].ticker.num_minor_ticks = 0
    p1.xaxis[0].ticker.num_minor_ticks = 0

    # build hover tooltip
    # todo - look into this more. probably not available for line glyphs
    hover = p1.select(dict(type=HoverTool))
    hover.point_policy = 'follow_mouse'
    hover.tooltips = OrderedDict([
        ('Value 1', "$x"),
        ('Value 2', "$y")
    ])

    script, div = components(p1)

    return render_template('main/index.html',
                           projects=projects,
                           script=script,
                           div=div)


