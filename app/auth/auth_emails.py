from app.utils.email_utils import email_client
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
    # Debug logging
    current_app.logger.info(f'Send reset password email called for user: {user.id}, email: {user.email}')
    
    if not user.email:
        current_app.logger.error(f'User {user.id} has no email address')
        raise ValueError("User has no email address")
    
    token = user.generate_token('reset_password')
    try:
        email_client.send_email(
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
        raise


def send_verification_email(user: 'User') -> None:
    """Send an email to the user with the account verification link

    Args:
        user (User)
    """
    # Debug logging
    current_app.logger.info(f'Send verification email called for user: {user.id}, email: {user.email}')
    
    if not user.email:
        current_app.logger.error(f'User {user.id} has no email address')
        raise ValueError("User has no email address")
    
    token = user.generate_token('verify_email')
    try:
        email_client.send_email(
            to_emails=user.email,
            subject='Verify your email',
            text_content=render_template(
                'auth/email/verify_email.txt',
                user=user,
                token=token
            ))
    except Exception as e:
        current_app.logger.exception(
            f'Error sending verification email: {e}')
        raise
