from flask import Blueprint


bp = Blueprint('clients', __name__, url_prefix='/clients')

from app.clients import client_routes  # noqa
