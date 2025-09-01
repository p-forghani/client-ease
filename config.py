import os
import logging
from pathlib import Path


base_dir = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'app.db')

    SALTS = {
        'reset_password': os.getenv('SECURITY_PASSWORD_SALT'),
        'verify_email': os.getenv('EMAIL_VERIFICATION_SALT')
    }
    ADMINS = ['forghani.dev@gmail.com']
    BREVO_SENDER_EMAIL = 'forghani.dev@gmail.com'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    LOG_FILE = os.path.join(base_dir, 'logs', 'app.log')
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.join(base_dir, 'logs'), exist_ok=True)


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    LOG_LEVEL = 'DEBUG'  # More verbose logging for tests


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'WARNING'
