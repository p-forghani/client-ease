from flask import flash, redirect, render_template, request, url_for
from app.utils import paginate_query
from flask_login import current_user

from app import db
from app.models import Client, Project
from app.project import bp
from app.project.prj_forms import ProjectForm


@bp.before_request
def before_request():
    """
    This function is executed before each request to the blueprint.
    It checks if the current user is authenticated.
    If the user is not authenticated, it redirects them to the login page.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))


# View all prj
@bp.route('/', methods=['GET'])
def view_all_projects():
    # Show a list of all the projects
    projects = paginate_query(
        query=Project.query.filter_by(user_id=current_user.id),
        request=request,
    )
    return render_template('project/index.html', projects=projects)


# Create prj
@bp.route('/create', methods=['GET', 'POST'])
def create_project():
    """Creates a project"""

    # TODO: What if some clients have same name

    form = ProjectForm()

    # TODO: Check if it is the most efficient way to get the clients
    # The first element of the tuple is the value that will be submitted with
    # the form, and the second element is the label that will be displayed to
    # the user.
    form.client.choices = [
        (client.id, client.name) for client in Client.query.filter_by(
            user_id=current_user.id).all()]
    # TODO: Instead of a drop down field for the client, use stringfield with
    # search and auto-complete and suggestion feature.
    if form.validate_on_submit():
        prj = Project(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            client_id=form.client.data,
            user_id=current_user.id
        )
        db.session.add(prj)
        db.session.commit()
        flash('Project Created Successfully!', category='success')
        return redirect(url_for('project.view_all_projects'))
    # Show the form
    return render_template(
        'project/create_project.html', form=form)


# Edit prj
@bp.route('/update/<prj_id>', methods=['GET', 'POST'])
def edit_project(prj_id):
    project = Project.query.get_or_404(prj_id)
    form = ProjectForm(obj=project)
    form.client.choices = [
        (client.id, client.name) for client in Client.query.filter_by(
            user_id=current_user.id).all()]
    if form.validate_on_submit():
        # Since client field is a select type, value it manually
        project.client_id = form.client.data
        # Remove client from form so populate_obj() ignores it
        del form._fields['client']
        # Populate other fields
        form.populate_obj(project)
        db.session.commit()
        flash('Project updated!', category='success')
        return redirect(url_for('project.view_project', prj_id=project.id))
    return render_template(
        template_name_or_list='project/create_project.html',
        form=form,
        project=project
    )


# View prj
@bp.route('/<prj_id>', methods=['GET'])
def view_project(prj_id):
    project = Project.query.get_or_404(prj_id)
    return render_template('project/view_project.html', project=project)


# Delete prj
@bp.route('/delete/<prj_id>', methods=['GET', 'POST'])
def delete_project(prj_id):
    project = Project.query.get_or_404(prj_id)
    db.session.delete(project)
    flash("Project deleted", category='info')
    return redirect(url_for('project.view_all_projects'))
