import stripe
from flask_login import current_user
from app.stripe.repo import (
    fetch_prices_by_ids,
)
import os


SERVER_URL = os.environ.get("SERVER_URL")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


def validate_price_ids(price_ids):
    prices = fetch_prices_by_ids(price_ids)
    if len(prices) != len(price_ids):
        raise Exception(f"One or more price IDs is not valid: {price_ids}")


def create_stripe_checkout_session_for_subscription(line_items):
    stripe.api_key = STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # Customer
        client_reference_id=current_user.id,
        customer=current_user.stripe_customer_id,
        # Payment
        allow_promotion_codes=True,
        payment_method_types=["card"],
        mode="subscription",
        line_items=line_items,
        # Callbacks
        success_url=f"{SERVER_URL}/#/success-payment",
        cancel_url=f"{SERVER_URL}/#/cancel-payment",
    )
    return checkout_session.url


# def create_stripe_checkout_session_for_one_off_purchase(line_items):
#     stripe.api_key = STRIPE_SECRET_KEY
#     checkout_session = stripe.checkout.Session.create(
#         # Customer
#         client_reference_id=current_user.id,
#         customer=current_user.stripe_customer_id,
#         # Payment
#         allow_promotion_codes=True,
#         payment_method_types=["card"],
#         mode="payment",
#         line_items=line_items,
#         # Callbacks
#         success_url=f"{SERVER_URL}/#/success",
#         cancel_url=f"{SERVER_URL}/#/cancel",
#     )

#     # Get the payment intent ID
#     payment_intent_id = checkout_session.payment_intent

#     # Here, insert a record into your own database to track the intended purchase.
#     # You will need to design this to fit your specific use case.
#     insert_purchase_intent(current_user.id, payment_intent_id, product_id)

#     return checkout_session.url
