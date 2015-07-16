import os, datetime
from app import db
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
        api_type = request.form['api_type']

        project = Project(
                          name=project_name,
                          api_type=api_type,
                          created_by=current_user.id
                        )
        db.session.add(project)
        db.session.commit()
        flash('Project Created')
        return redirect(url_for('main_site_index.index'))

    return render_template('main/api_auth.html', form=form)

