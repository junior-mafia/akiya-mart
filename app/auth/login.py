from app.user.repo import fetch_user_by_email, update_last_logged_in_at
from app.extensions import bcrypt
from flask_login import login_user


class IncorrectPasswordException(Exception):
    pass


class EmailNotFoundException(Exception):
    pass


def log_in_user(email, password_candidate):
    user = fetch_user_by_email(email)
    if user is None:
        raise EmailNotFoundException(
            f"User not found by email during login attempt: {email}"
        )

    if not bcrypt.check_password_hash(user.hashed_password, password_candidate):
        raise IncorrectPasswordException("Incorrect password")

    login_user(user)
    update_last_logged_in_at(user.id)