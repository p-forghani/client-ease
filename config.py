import os
from pathlib import Path


base_dir = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'app.db')

    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
    ADMINS = ['forghani.dev@gmail.com']
