from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth import bp as auth_bp
    from app.client import bp as client_bp
    from app.main import bp as main_bp
    from app.admin import bp as admin_bp
    from app.project import bp as prj_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(prj_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app

from app import models  # noqa
