from app.invoice import bp
from app.models import Project
from app import db
from app.models import Invoice
from app.invoice.inv_forms import InvoiceForm
from flask import request
from flask import redirect, url_for, flash, render_template
from flask_login import current_user


@bp.before_request
def before_request():
    """
    This function is executed before each request to the blueprint.
    It checks if the current user is authenticated.
    If the user is not authenticated, it redirects them to the login page.
    """
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))


@bp.route('/', methods=['GET'])
def get_invoices():
    invoices = Invoice.query.filter_by(
        user_id=current_user.id).paginate(
            page=request.args.get('page', 1, type=int),
            per_page=request.args.get('per_page', 10, type=int),
    )
    return render_template(
        'invoice/index.html',
        invoices=invoices,
    )


@bp.route('/edit/<int:id>', methods=['GET', 'PUT'])
def update_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    if (not invoice) or (invoice.project.user_id != current_user.id):
        return 'You are not authorized to view this invoice', 403
    form = InvoiceForm(obj=invoice)
    if form.validate_on_submit():
        form.populate_obj(invoice)
        db.session.commit()
        flash('Invoice updated successfully', 'success')
        return redirect(url_for('invoice.view_invoice', id=invoice.id))
    # if get: show invoice form
    return render_template(
        'invoice/invoice_form.html',
        form=form,
        invoice=invoice
    )


@bp.route('/<int:id>', methods=['DELETE'])
def delete_invoice(id):
    # TODO: Ask confirmation before deleting (user AJAX)
    invoice = Invoice.query.get_or_404(id)
    if (not invoice) or (invoice.project.user_id != current_user.id):
        return 'You are not authorized to view this invoice', 403

    db.session.delete(invoice)
    db.session.commit()
    flash('Invoice deleted successfully', 'success')
    # TODO: Redirect to the project page
    return redirect(url_for('main.index'))


@bp.route('/<int:id>', methods=['GET'])
def view_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    if (not invoice) or (invoice.project.user_id != current_user.id):
        return 'You are not authorized to view this invoice', 403
    return render_template('invoice/invoice.html', invoice=invoice)


@bp.route('/create', methods=['GET', 'POST'])
def create_invoice():
    # the project id will be passed in the get request
    project = Project.query.get_or_404(request.args.get('project_id'))
    # Since I am using get_or_404, it is impossible for project to be None
    if project.user_id != current_user.id:
        return (
            'You are not authorized to create an invoice for this project',
            403
        )

    form = InvoiceForm()
    if form.validate_on_submit():
        invoice = Invoice(
            project_id=project.id,
            user_id=current_user.id,
            client_id=project.client_id,
            date=form.date.data,
            amount=form.amount.data,
            description=form.description.data,
            status=form.status.data
        )
        db.session.add(invoice)
        db.session.commit()
        flash('Invoice created successfully', 'success')
        return redirect(url_for('invoice.view_invoice', id=invoice.id))
    # if it is get request render template for invoice form
    return render_template(
        'invoice/invoice_form.html',
        form=form,
        project_id=project.id)
