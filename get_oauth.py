from aggtron import db
from models import Project, Users, AuthInfo
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, redirect, flash


get_oauth = Blueprint('get_oauth', __name__, template_folder='templates')