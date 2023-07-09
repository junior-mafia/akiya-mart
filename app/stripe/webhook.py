from app.stripe.price import create_or_update_price
from app.stripe.product import create_or_update_product
from app.stripe.subscription import (
    create_customer_subscription,
    update_customer_subscription,
)
from app.stripe.coupon import create_or_update_coupon
from app.stripe.promotion_code import (
    create_or_update_promotion_code,
)
import stripe


def process_event(event):
    event_type = event["type"]
    if event_type == "customer.subscription.created":
        create_customer_subscription(event)
    elif event_type == "customer.subscription.updated":
        update_customer_subscription(event)
    elif event_type == "customer.subscription.deleted":
        update_customer_subscription(event)
    elif event_type == "product.created":
        create_or_update_product(event)
    elif event_type == "product.updated":
        create_or_update_product(event)
    elif event_type == "product.deleted":
        create_or_update_product(event)
    elif event_type == "price.created":
        create_or_update_price(event)
    elif event_type == "price.updated":
        create_or_update_price(event)
    elif event_type == "price.deleted":
        create_or_update_price(event)
    elif event_type == "coupon.created":
        create_or_update_coupon(event)
    elif event_type == "coupon.updated":
        create_or_update_coupon(event)
    elif event_type == "coupon.deleted":
        create_or_update_coupon(event)
    elif event_type == "promotion_code.created":
        create_or_update_promotion_code(event)
    elif event_type == "promotion_code.updated":
        create_or_update_promotion_code(event)
    elif event_type == "promotion_code.deleted":
        create_or_update_promotion_code(event)


def validate_stripe_event(payload, sig_header, endpoint_secret):
    event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    return event
