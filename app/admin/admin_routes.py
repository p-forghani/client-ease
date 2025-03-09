from app import db
from app.models import User
from app.decorators import admin_only
from app.admin import bp


# TODO: Implement the CRUD routes for the Role model


# View users list for admin only
@bp.route('/users')
@admin_only
def user_list():
    users = db.session.execute(db.select(User)).scalars().all()
    return [user.first_name for user in users]
