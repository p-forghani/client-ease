from flask import (current_app, flash, redirect, render_template, request,
                   url_for, abort)
from app.utils.db import paginate_query, search_in_query
from flask_login import current_user
from sqlalchemy.orm import joinedload

from app import db
from app.client import bp
from app.client.client_forms import CreateClientForm, UpdateClientForm
from app.models import Client
from app.utils.logger import log_user_action, log_error


# Instead of using the @login_required decorator, we use this function to
# check if the user is authenticated
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
        flash('Please verify your email address to access clients.', 
              category='warning')
        return redirect(url_for('auth.verification_reminder'))


@bp.route('/')
def index():
    """Shows the list of the clients"""
    current_app.logger.info('/client/ route called')
    # Filter clients based on user_id and optionally search_query
    clients = paginate_query(
        query=search_in_query(
            query=Client.query.filter_by(user_id=current_user.id),
            request=request,
            fields=(Client.name, Client.email, Client.phone, Client.address)
        ),
        request=request
    )
    return render_template(
        'client/index.html',
        clients=clients,
    )


@bp.route('/add', methods=['GET', 'POST'])
def add_client():
    '''Add a new client'''
    form = CreateClientForm()
    if form.validate_on_submit():
        client = Client()
        client.name = form.name.data
        client.address = form.address.data
        client.phone = form.phone.data
        client.email = form.email.data.lower()
        client.user_id = current_user.id
        db.session.add(client)
        db.session.commit()
        flash('Client added successfully', category='success')
        return redirect(url_for('client.index'))
    # Show the form
    return render_template('client/add_client.html', form=form)


@bp.route('/<client_id>')
def view_client(client_id):
    client = Client.query.options(
        joinedload(Client.projects),
        joinedload(Client.invoices),
        ).get_or_404(client_id)
    return render_template('client/view_client.html', client=client)


@bp.route('/<client_id>/edit', methods=['GET', 'POST'])
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    form = UpdateClientForm(obj=client)
    if form.validate_on_submit():
        form.populate_obj(client)
        db.session.commit()
        flash('Client updated successfully', 'success')
        return redirect(url_for('client.view_client', client_id=client.id))
    return render_template('client/update_client.html', form=form,
                           client=client)


@bp.route('/<client_id>/delete', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    
    # Check authorization
    if client.user_id != current_user.id:
        log_error('Unauthorized client deletion attempt', 
                 user_id=current_user.id, 
                 client_id=client_id, 
                 ip_address=request.remote_addr)
        # Always return error page for unauthorized access
        abort(403)

    try:
        # Log the deletion action
        log_user_action(
            'client_deleted',
            user_id=current_user.id,
            client_id=client.id,
            client_name=client.name,
            ip_address=request.remote_addr
        )
        
        db.session.delete(client)
        db.session.commit()
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'message': 'Client deleted successfully'}, 200
        else:
            flash('Client deleted successfully', 'success')
            return redirect(url_for('client.index'))
            
    except Exception as e:
        db.session.rollback()
        log_error('Failed to delete client', 
                 error=e, 
                 user_id=current_user.id, 
                 client_id=client_id)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {'error': 'Failed to delete client'}, 500
        else:
            abort(500)
