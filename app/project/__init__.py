from flask import Blueprint


bp = Blueprint('project', __name__, url_prefix='/project')

from app.project import prj_routes  # noqa