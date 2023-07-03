from app.extensions import bcrypt
from app.user.repo import insert_user, fetch_user_by_email, update_last_logged_in_at
from flask_login import login_user
import os
import stripe


STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")


def register_user(email, password):
    stripe.api_key = STRIPE_SECRET_KEY
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    stripe_customer = stripe.Customer.create(email=email)
    user_data = {
        "email": email,
        "hashed_password": hashed_password,
        "stripe_customer_id": stripe_customer.id,
    }
    insert_user(user_data)

    user = fetch_user_by_email(email)
    if user is None:
        raise Exception(
            f"User not found by email during registration attempt: {email}"
        )

    login_user(user)
    update_last_logged_in_at(user.id)
