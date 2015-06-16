import os, datetime
from flask import Blueprint, render_template, url_for, request, redirect
from flask.ext.login import (current_user, login_required)
from aggtron.models import AuthPass, Project
from forms import ProjectForm
from libs.User import User


add_project = Blueprint('add_project', __name__, template_folder='templates')


@add_project.route('/create', methods=['GET', 'POST'])
@login_required
def index():
    form = ProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        project_name = request.form['name']
        project = Project(
                          name=project_name,
                          database='test_db',
                          created_by=str(current_user.email)
                    )
        project.save()
        return redirect('/')

    return render_template('api_auth.html')

# todo - works manually saving data in shell, but not on form submit