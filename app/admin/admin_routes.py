from app import db
from app.models import User
from app.utils.decorators import admin_only
from app.admin import bp
from flask import request, render_template


# FUTURE: Implement the CRUD routes for the Role model


# View users list for admin only
@bp.route('/users')
@admin_only
def user_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    users = User.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/users.html', users=users)
