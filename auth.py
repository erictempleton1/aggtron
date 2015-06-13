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


@auth_flask_login.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = forms.SignupForm(request.form)
    current_app.logger.info(request.form)

    if request.method == 'POST' and registerForm.validate() == False:
        current_app.logger.info(registerForm.errors)
        return 'registration error'
    elif request.method == 'POST' and registerForm.validate():
        email = request.form['email']

        # create password hash
        password_hash = flask_bcrypt.generate_password_hash(request.form['password'])

        # prepare user
        user = User(email, password_hash)
        print user

        try:
            user.save()
            if login_user(user, remember='no'):
                flash('Logged in')
                return redirect('/')
            else:
                flash('Unable to login')
        except:
            flash('Unable to register with given email address')
            current_app.logger.error('Error on registeration - possible duplicate emails')

    templateData = {'form': registerForm}

    return render_template('/auth/register.html', **templateData)