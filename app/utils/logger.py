"""
Logging utilities for the ClientEase application.
Provides consistent logging functions and error handling.
"""

from flask import current_app
import logging


def log_info(message, **kwargs):
    """Log an info message with optional context."""
    if kwargs:
        message = f"{message} | Context: {kwargs}"
    current_app.logger.info(message)


def log_warning(message, **kwargs):
    """Log a warning message with optional context."""
    if kwargs:
        message = f"{message} | Context: {kwargs}"
    current_app.logger.warning(message)


def log_error(message, error=None, **kwargs):
    """Log an error message with optional exception and context."""
    if error:
        message = f"{message} | Error: {str(error)}"
    if kwargs:
        message = f"{message} | Context: {kwargs}"
    current_app.logger.error(message, exc_info=error is not None)


def log_debug(message, **kwargs):
    """Log a debug message with optional context."""
    if kwargs:
        message = f"{message} | Context: {kwargs}"
    current_app.logger.debug(message)


def log_user_action(action, user_id=None, **kwargs):
    """Log user actions for audit purposes."""
    context = {'action': action}
    if user_id:
        context['user_id'] = user_id
    context.update(kwargs)
    current_app.logger.info(f"User action: {action}", extra=context)


def log_security_event(event, user_id=None, ip_address=None, **kwargs):
    """Log security-related events."""
    context = {'event': event, 'security_event': True}
    if user_id:
        context['user_id'] = user_id
    if ip_address:
        context['ip_address'] = ip_address
    context.update(kwargs)
    current_app.logger.warning(f"Security event: {event}", extra=context)
