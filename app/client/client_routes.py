from flask import current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.client import bp
from app.client.client_forms import CreateClientForm, UpdateClientForm
from app.models import Client


@bp.route('/')
@login_required
def index():
    "Show the list of clients"
    current_app.logger.info('Index route called')
    clients = Client.query.filter_by(user_id=current_user.id).all()
    # Use pagination to limit the number of clients displayed
    return render_template('client/index.html', clients=clients)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
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
@login_required
def view_client(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('client/view_client.html', client=client)


@bp.route('/<client_id>/edit', methods=['GET', 'POST'])
@login_required
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
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client deleted successfully')
    return redirect(url_for('client.index'))
