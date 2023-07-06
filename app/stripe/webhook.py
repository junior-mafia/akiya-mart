from app.stripe.price import (
    handle_price_created,
    handle_price_updated,
)
from app.stripe.product import (
    handle_product_created,
    handle_product_updated,
)
from app.stripe.subscription import (
    handle_customer_subscription_created,
    handle_customer_subscription_updated,
)
import stripe


def process_event(event):
    event_type = event["type"]
    if event_type == "customer.subscription.created":
        handle_customer_subscription_created(event)
    elif event_type == "customer.subscription.updated":
        handle_customer_subscription_updated(event)
    elif event_type == "customer.subscription.deleted":
        handle_customer_subscription_updated(event)
    elif event_type == "payment_intent.succeeded":
        # handle_payment_intent(event)
        pass
    elif event_type == "payment_intent.payment_failed":
        # handle_payment_intent(event)
        pass
    elif event_type == "product.created":
        handle_product_created(event)
    elif event_type == "product.updated":
        handle_product_updated(event)
    elif event_type == "product.deleted":
        handle_product_updated(event)
    elif event_type == "price.created":
        handle_price_created(event)
    elif event_type == "price.updated":
        handle_price_updated(event)
    elif event_type == "price.deleted":
        handle_price_updated(event)


def validate_stripe_event(payload, sig_header, endpoint_secret):
    event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    return event
