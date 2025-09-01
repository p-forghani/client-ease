from flask import flash, redirect, render_template, request, url_for, current_app, abort
from app.utils.db import paginate_query, search_in_query
from flask_login import current_user

from app import db
from app.models import Client, Project
from app.project import bp
from app.project.prj_forms import ProjectForm
from app.utils.logger import log_user_action, log_error


@bp.before_request
def before_request():
    """
    This function is executed before each request to the blueprint.
    It checks if the current user is authenticated and email verified.
    If the user is not authenticated, it redirects them to the login page.
    If the user's email is not verified, it redirects them to verification reminder.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    # Check if user's email is verified
    if not current_user.email_verified:
        flash('Please verify your email address to access projects.',
              category='warning')
        return redirect(url_for('auth.verification_reminder'))


# View all prj
@bp.route('/', methods=['GET'])
def view_all_projects():
    # Show a list of all the projects
    projects = paginate_query(
        query=search_in_query(
            query=Project.query.join(Client).filter_by(
                user_id=current_user.id),
            request=request,
            fields=(Project.title, Project.description, Client.name)),
        request=request
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
        prj = Project()
        prj.title = form.title.data
        prj.description = form.description.data
        prj.start_date = form.start_date.data
        prj.end_date = form.end_date.data
        prj.client_id = form.client.data
        prj.user_id = current_user.id
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
@bp.route('/delete/<prj_id>', methods=['DELETE'])
def delete_project(prj_id):
    project = Project.query.get_or_404(prj_id)

    # Check authorization
    if project.user_id != current_user.id:
        log_error('Unauthorized project deletion attempt', 
                 user_id=current_user.id,
                 project_id=prj_id,
                 ip_address=request.remote_addr)
        # Always return error page for unauthorized access
        abort(403)

    try:
        # Log the deletion action
        log_user_action(
            'project_deleted',
            user_id=current_user.id,
            project_id=project.id,
            project_title=project.title,
            client_name=project.client.name,
            ip_address=request.remote_addr
        )

        db.session.delete(project)
        db.session.commit()

        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'message': 'Project deleted successfully'}, 200
        else:
            flash('Project deleted successfully', 'success')
            return redirect(url_for('project.view_all_projects'))

    except Exception as e:
        db.session.rollback()
        log_error('Failed to delete project',
                 error=e,
                 user_id=current_user.id,
                 project_id=prj_id)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'error': 'Failed to delete project'}, 500
        else:
            abort(500)
