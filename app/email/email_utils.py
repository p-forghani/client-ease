# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import current_app

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
except Exception as e:
    current_app.logger.error(f'Error creating SendGridAPIClient: {e}')


# TODO: take from_email as an argument
def send_email(to_emails, subject, html_content=None, text_content=None):
    message = Mail(
        from_email='forghani.dev@gmail.com',
        to_emails=to_emails,
        subject=subject,
        html_content=html_content,
        plain_text_content=text_content
    )
    try:
        response = sg.send(message)
        current_app.logger.info(f'Email sent: {response.status_code}')
    except Exception as e:
        current_app.logger.error(f'Error sending email: {e}')
        return False
    return True

