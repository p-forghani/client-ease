# Description: This file contains decorators for the application.
import functools

from flask import abort
from flask_login import current_user


def admin_only(view_function):
    """
    Decorator to restrict access to admin-only views.

    This decorator checks if the current user has an admin role (role_id == 1).
    If the user is not an admin, it aborts the request with a 403 Forbidden
    status. Otherwise, it allows the view function to be executed.

    Args:
        view_function (function): The view function to be decorated.

    Returns:
        function: The wrapped view function with admin-only access control.
    """
    @functools.wraps(view_function)
    def wrapper(*args, **kwargs):
        # Check if current_user is Admin
        if not current_user.is_authenticated or \
           not current_user.role_id == 1:
            abort(403)
            return
        return view_function(*args, **kwargs)
    return wrapper
