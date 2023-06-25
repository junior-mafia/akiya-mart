from app.extensions import bcrypt
from app.auth.repo import insert_user
from app.auth.repo import fetch_user_by_email
from flask_login import login_user


def handle_register(email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user_data = {
        "email": email,
        "hashed_password": hashed_password,
    }

    _, error = insert_user(user_data)
    if error:
        return None, error

    user, error = fetch_user_by_email(email)
    if error:
        return None, error
    if user is None:
        return None, "Email not found"

    login_user(user)

    return None, None
