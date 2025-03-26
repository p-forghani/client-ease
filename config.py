import os
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
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE'))
