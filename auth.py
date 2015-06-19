import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for, request, abort
from jinja2 import TemplateNotFound
from aggtron import login_manager, flask_bcrypt, db, mongo
from models import User, AuthPass, Project
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

from forms import LoginForm, SignupForm
from libs.User import User
from flask.ext.mongoengine import MongoEngine


auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates')


@auth_flask_login.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        user = mongo.db.user.find_one({'email': email})
        if user and flask_bcrypt.check_password_hash(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)

            return redirect('/')
        else:
            redirect('http://www.google.com')
    return render_template('/auth/login.html', form=form)


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


@auth_flask_login.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out')
    return redirect('/login')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_user(email):
    user = mongo.db.user.find_one({'email': email})
    if not user:
        return None
    return unicode(user['_id'])