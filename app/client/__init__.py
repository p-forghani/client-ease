from flask import Blueprint


bp = Blueprint('client', __name__, url_prefix='/client')


from app.client import client_routes  # noqa
