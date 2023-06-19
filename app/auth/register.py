from app.extensions import bcrypt
from app.auth.repo import insert_user


def handle_register(email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = {
        "email": email,
        "hashed_password": hashed_password,
    }

    _, error = insert_user(user)
    if error:
        return None, error

    return None, None
