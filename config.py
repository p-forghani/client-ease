import os
import logging
from pathlib import Path
from dotenv import load_dotenv


base_dir = Path(__file__).resolve().parent
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    db_url = os.getenv('DATABASE_URL')
    
    # Require PostgreSQL connection - raise error if not available
    if not db_url:
        raise ValueError(
            "DATABASE_URL environment variable is required. "
            "Please provide a PostgreSQL connection string."
        )
    
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    # Validate that it's a PostgreSQL connection
    if not db_url.startswith('postgresql://'):
        raise ValueError(
            "Only PostgreSQL database connections are supported. "
            f"Provided URL: {db_url[:20]}..."
        )
    
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
