from flask import (current_app, flash, redirect, render_template, request,
                   url_for)
from app.utils import paginate_query
from flask_login import current_user

from app import db
from app.client import bp
from app.client.client_forms import CreateClientForm, UpdateClientForm
from app.models import Client


@bp.before_request
def before_request():
    """
    This function is executed before each request to the blueprint.
    It checks if the current user is authenticated.
    If the user is not authenticated, it redirects them to the login page.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))


@bp.route('/')
def index():
    """Shows the list of the clients"""
    current_app.logger.info('/client/ route called')
    clients = paginate_query(
        query=Client.query.filter_by(user_id=current_user.id),
        request=request,
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
        client = Client(
            name=form.name.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data,
            user_id=current_user.id
        )
        db.session.add(client)
        db.session.commit()
        flash('Client added successfully')
        return redirect(url_for('client.index'))
    # Show the form
    return render_template('client/add_client.html', form=form)


@bp.route('/<client_id>')
def view_client(client_id):
    client = Client.query.get_or_404(client_id)
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


@bp.route('/<client_id>/delete', methods=['POST'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client deleted successfully')
    return redirect(url_for('client.index'))
