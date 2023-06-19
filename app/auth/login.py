from app.auth.repo import fetch_user_by_email
from app.extensions import bcrypt
from flask_login import login_user

def handle_login(email, password_candidate):
    user, error = fetch_user_by_email(email)
    if error:
        return None, error
    if user is None:
        return None, "User not found"

    if not bcrypt.check_password_hash(user.hashed_password, password_candidate):
        return None, "Incorrect password"

    login_user(user)

    return None, None
