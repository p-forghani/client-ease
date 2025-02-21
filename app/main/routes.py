from flask import current_app
from flask_login import login_required

from app.main import bp


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    current_app.logger.info('Index route called')
    return "Hello, World!"
