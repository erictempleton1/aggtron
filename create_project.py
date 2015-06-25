import os, datetime
from flask import Blueprint, render_template, url_for, request, redirect
from forms import ProjectForm
from flask.ext.login import (current_user, login_required, login_user,
                             logout_user, confirm_login, fresh_login_required)



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
                          created_by=current_user.get_mongo_doc()
                    )
        project.save()
        return redirect('/create')

    return render_template('api_auth.html')

