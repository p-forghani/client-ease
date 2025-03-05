import os
import threading

from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
except Exception as e:
    current_app.logger.error(f'Error creating SendGridAPIClient: {e}')


def send_async_email(app, msg):
    """Sends email in a separate thread."""
    with app.app_context():  # Needed for Flask to work inside threads
        sg.send(msg)
        current_app.logger.info('Email sent Successfully')


def send_email(
        from_email, to_emails, subject, html_content=None, text_content=None
):
    # Get the real Flask app instance
    app = current_app._get_current_object()

    message = Mail(
        from_email=from_email,
        to_emails=to_emails,
        subject=subject,
        html_content=html_content,
        plain_text_content=text_content
    )
    try:
        thread = threading.Thread(target=send_async_email, args=(app, message))
        thread.start()
    except Exception as e:
        current_app.logger.error(f'Error sending email: {e}')
        return False
    return True
