import config
import requests
from app import db
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, request, flash, redirect, url_for


build_soql = Blueprint('build_soql', __name__, template_folder='templates')