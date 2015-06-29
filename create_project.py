import os, datetime
from aggtron import db
from forms import ProjectForm
from models import Project, Users
from flask.ext.login import current_user, login_required
from flask import Blueprint, render_template, url_for, request, redirect, flash



add_project = Blueprint('add_project', __name__, template_folder='templates')


@add_project.route('/create', methods=['GET', 'POST'])
@login_required
def index():
    form = ProjectForm()
    if form.validate_on_submit():
        project_name = request.form['name']

        project = Project(
                          name=project_name,
                          created_by=current_user.id
                        )
        db.session.add(project)
        db.session.commit()
        flash('Project Created')
        return redirect('/create')

    return render_template('api_auth.html', form=form)

