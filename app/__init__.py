from flask import Flask
from config import Config
from app.extensions import db, bcrypt, login_manager
from app.user.repo import fetch_user_by_id
from celery import Celery
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
if BROKER_URL != "redis://localhost:6379/0":
    BROKER_URL += "?ssl_cert_reqs=CERT_NONE"


celery = Celery(__name__, broker=BROKER_URL)


# Database setup for Celery tasks
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="build")
    app.config.from_object(config_class)

    # Db extension
    db.init_app(app)
    with app.app_context():
        db.reflect()

    # Login extension
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Celery configuration
    celery.conf.update(app.config)

    # Register blueprints here
    from app.home import bp as bp_home

    app.register_blueprint(bp_home)

    from app.auth import bp as bp_auth

    app.register_blueprint(bp_auth, url_prefix="/auth")

    from app.stripe import bp as bp_stripe

    app.register_blueprint(bp_stripe, url_prefix="/stripe")

    from app.user import bp as bp_user

    app.register_blueprint(bp_user, url_prefix="/user")

    from app.listings import bp as bp_listings

    app.register_blueprint(bp_listings, url_prefix="/listings")

    from app.admin import bp as bp_admin

    app.register_blueprint(bp_admin, url_prefix="/admin")

    return app


@login_manager.user_loader
def load_user(user_id):
    # This is for flask-login so we are forced to ignore errors
    user = fetch_user_by_id(user_id)
    return user
