from flask import Flask
from config import Config
from app.extensions import db, bcrypt, login_manager
from app.extensions import login_manager
from app.user.repo import fetch_user_by_id


def create_app(config_class=Config):
    app = Flask(__name__, static_folder="build")
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    with app.app_context():
        db.reflect()
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register blueprints here
    from app.home import bp as bp_home

    app.register_blueprint(bp_home)

    from app.auth import bp as bp_auth

    app.register_blueprint(bp_auth, url_prefix="/auth")

    from app.stripe import bp as bp_stripe

    app.register_blueprint(bp_stripe, url_prefix="/stripe")

    from app.user import bp as bp_user

    app.register_blueprint(bp_user, url_prefix="/user")

    return app


@login_manager.user_loader
def load_user(user_id):
    # This is for flask-login so we are forced to ignore errors
    user = fetch_user_by_id(user_id)
    return user
