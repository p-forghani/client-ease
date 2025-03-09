from flask import Blueprint


bp = Blueprint('auth', __name__, url_prefix='/auth')

# Import the views to register them with the blueprint
from app.auth import auth_routes  # noqa
