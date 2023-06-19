from flask import Flask
from config import Config
from app.extensions import db, bcrypt, login_manager
from app.extensions import login_manager
from app.auth.repo import fetch_user_by_id

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    with app.app_context():
        db.reflect()
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Register blueprints here
    from app.main import bp as bp_main

    app.register_blueprint(bp_main)

    from app.auth import bp as bp_auth

    app.register_blueprint(bp_auth, url_prefix="/auth")

    return app

@login_manager.user_loader
def load_user(user_id):
    # This is for flask-login so we are forced to ignore errors
    user, _ = fetch_user_by_id(user_id)
    return user