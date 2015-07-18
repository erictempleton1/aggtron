from flask import current_app, Blueprint, render_template, request, flash, redirect, url_for
from app import login_manager, flask_bcrypt, db
from models import Users
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from forms import LoginForm, SignupForm


auth_flask_login = Blueprint('auth_flask_login', __name__, template_folder='templates')


@auth_flask_login.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()

        if user and flask_bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged In')
            return redirect('/')    

    return render_template('auth/login.html', form=form)


@auth_flask_login.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']

        # create password hash
        password_hash = flask_bcrypt.generate_password_hash(password)

        # prepare user
        user = Users(email=email, password=password_hash)

        try:
            db.session.add(user)
            db.session.commit()
            if login_user(user, remember='no'):
                flash('Account Created & Logged in')
                return redirect('/')
            else:
                flash('Unable to login')
        except:
            flash('Unable to register with given email address')
            current_app.logger.error('Error on registeration - possible duplicate emails')

    return render_template('/auth/register.html', form=form)


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
def load_user(id):
    return Users.query.get(int(id))