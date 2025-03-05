from app.email import send_email
from flask import current_app, render_template
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User


def send_reset_password_email(user: 'User') -> None:
    """
    Send an email to the user with the reset password link

    :param user: user object
    :return: None
    """
    token = user.generate_reset_password_token()
    try:
        send_email(
            from_email=current_app.config['ADMINS'][0],
            to_emails=user.email,
            subject='Reset Password',
            text_content=render_template(
                'auth/email/reset_password.txt',
                user=user,
                token=token
            ))
    except Exception as e:
        current_app.logger.exception(
            f'Error sending reset password email: {e}')
