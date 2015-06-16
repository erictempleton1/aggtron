import os, datetime
from flask import Blueprint, render_template, url_for, request
from flask.ext.login import (current_user, login_required)
from aggtron.models import AuthPass, Project

import forms
from libs.User import User


add_project = Blueprint('add_project', __name__, template_folder='templates')


@add_project.route('/create', methods=['GET', 'POST'])
@login_required
def index():
    form = forms.ProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        project = Project(
                          name='test',
                          database='test_db',
                          created_by='test'
                    )
        project.save()
        return redirect('/')

    return render_template('api_auth.html')

# todo - fix template inheritence & add forms