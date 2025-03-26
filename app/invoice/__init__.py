from flask import Blueprint

bp = Blueprint('invoice', __name__, url_prefix='/invoice')

from app.invoice import inv_routes  # noqa
