import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from jinja2 import TemplateNotFound
from aggtron import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

import forms
from libs.User import User


auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates')


@auth_flask_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and email in request.form:
        email = request.form['email']
        userObj = User()
        user = userObj.get_by_email_w_password(email)
        if user and flask_bcrypt.check_password_hash(user.password, request.form['password']) and user.is_active():
            remember = request.form.get('remember', 'no') == 'yes'

            if login_user(user, remember=remember):
                flash('Logged in')
            else:
                flash('Unable to log in')

    return render_template('/auth/login.html')