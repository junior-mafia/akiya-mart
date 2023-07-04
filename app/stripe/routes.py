from app.stripe import bp
from flask import request, jsonify, current_app as app
import stripe
import os
from flask_login import login_required, current_user
from app.stripe.repo import (
    fetch_stripe_event_by_id,
    create_subscription,
    insert_or_update_invoice,
    fetch_prices_by_ids,
    insert_product,
    insert_price,
    update_product,
    update_price,
    delete_product,
    delete_price,
    fetch_all_items,
)
from app.user.repo import fetch_user_by_id, fetch_user_by_stripe_customer_id
import traceback
from datetime import datetime


SERVER_URL = os.environ.get("SERVER_URL")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


def validate_price_ids(price_ids):
    prices = fetch_prices_by_ids(price_ids)
    if len(prices) != len(price_ids):
        raise Exception(f"One or more price IDs is not valid: {price_ids}")


def create_stripe_checkout_session(line_items):
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
        success_url=f"{SERVER_URL}/#/success",
        cancel_url=f"{SERVER_URL}/#/cancel",
    )
    return checkout_session.url


@bp.route("/create-checkout-session", methods=["POST"])
@login_required
def create_checkout_session():
    try:
        data = request.get_json()
        price_ids = data.get("priceIds")
        validate_price_ids(price_ids)
        line_items = [{"price": price_id, "quantity": 1} for price_id in price_ids]

        user = fetch_user_by_id(current_user.id)
        if user is None:
            raise Exception(f"User not found with id: {current_user.id}")

        url = create_stripe_checkout_session(line_items)
        result = {"url": url}
        return jsonify({"success": True, "result": result}), 200
    except Exception as e:
        error = f"Exception during creation of Stripe checkout session: {str(e)}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500











def handle_customer_subscription_created(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    subscription = event["data"]["object"]
    subscription_id = subscription["id"]
    customer_id = subscription["customer"]
    user = fetch_user_by_stripe_customer_id(customer_id)
    subscription_record = {
        "subscription_id": subscription_id,
        "user_id": user.id,
        "created_at": event_timestamp,
        "updated_at": event_timestamp,
    }

    line_items = subscription["items"]["data"]
    subscription_item_records = []
    for line_item in line_items:
        price_id = line_item["price"]["id"]
        subscription_item_record = {
            "subscription_id": subscription_id,
            "price_id": price_id,
            "created_at": event_timestamp,
            "updated_at": event_timestamp,
        }
        subscription_item_records.append(subscription_item_record)

    create_subscription(event, subscription_record, subscription_item_records)


def handle_invoice_payment_succeeded(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    invoice = event["data"]["object"]
    invoice_id = invoice["id"]
    subscription_id = invoice["subscription"]
    currency = invoice["currency"]
    amount_due = invoice["amount_due"]
    amount_paid = invoice["amount_paid"]
    invoice_record = {
        "invoice_id": invoice_id,
        "subscription_id": subscription_id,
        "currency": currency,
        "amount_due": amount_due,
        "amount_paid": amount_paid,
        "created_at": event_timestamp,
        "updated_at": event_timestamp,
    }

    insert_or_update_invoice(invoice_record)



def handle_invoice_payment_failed(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    invoice = event["data"]["object"]
    invoice_id = invoice["id"]
    subscription_id = invoice["subscription"]
    currency = invoice["currency"]
    amount_due = invoice["amount_due"]
    amount_paid = invoice["amount_paid"]
    invoice_record = {
        "invoice_id": invoice_id,
        "subscription_id": subscription_id,
        "currency": currency,
        "amount_due": amount_due,
        "amount_paid": amount_paid,
        "created_at": event_timestamp,
        "updated_at": event_timestamp,
    }

    insert_or_update_invoice(invoice_record)


def handle_customer_subscription_deleted(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    # subscription = event["data"]["object"]
    # subscription_id = subscription["id"]
    # deactivate_subscription(subscription_id)
    pass


def handle_product_created(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    product_data = event["data"]["object"]
    product_record = {
        "product_id": product_data["id"],
        "name": product_data["name"],
        "description": product_data["description"],
        "now": event_timestamp,
    }
    insert_product(product_record)


def handle_product_updated(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    product_data = event["data"]["object"]
    product_record = {
        "product_id": product_data["id"],
        "name": product_data["name"],
        "description": product_data["description"],
        "now": event_timestamp,
    }
    update_product(product_record)


def handle_product_deleted(event):
    product_data = event["data"]["object"]
    product_id = product_data["id"]
    delete_product(product_id)


def handle_price_created(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    price_data = event["data"]["object"]
    recurring = price_data.get("recurring", {})
    price_record = {
        "price_id": price_data["id"],
        "product_id": price_data["product"],
        "currency": price_data["currency"],
        "unit_amount": price_data["unit_amount"],
        "recurring_interval": recurring.get("interval") if recurring else None,
        "now": event_timestamp,
    }
    insert_price(price_record)


def handle_price_updated(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    price_data = event["data"]["object"]
    recurring = price_data.get("recurring", {})
    price_record = {
        "price_id": price_data["id"],
        "product_id": price_data["product"],
        "currency": price_data["currency"],
        "unit_amount": price_data["unit_amount"],
        "recurring_interval": recurring.get("interval") if recurring else None,
        "now": event_timestamp,
    }
    update_price(price_record)


def handle_price_deleted(event):
    price_data = event["data"]["object"]
    price_id = price_data["id"]
    delete_price(price_id)


def process_event(event):
    event_type = event["type"]
    if event_type == "customer.subscription.created":
        handle_customer_subscription_created(event)
    elif event_type == "customer.subscription.deleted":
        handle_customer_subscription_deleted(event)
    elif event_type == "invoice.payment_succeeded":
        handle_invoice_payment_succeeded(event)
    elif event_type == "invoice.payment_failed":
        handle_invoice_payment_failed(event)
    elif event_type == "product.created":
        handle_product_created(event)
    elif event_type == "product.updated":
        handle_product_updated(event)
    elif event_type == "product.deleted":
        handle_product_deleted(event)
    elif event_type == "price.created":
        handle_price_created(event)
    elif event_type == "price.updated":
        handle_price_updated(event)
    elif event_type == "price.deleted":
        handle_price_deleted(event)


def validate_stripe_event(payload, sig_header, endpoint_secret):
    event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    return event


@bp.route("/webhook", methods=["POST"])
def webhook():
    try:
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get("Stripe-Signature")
        event = validate_stripe_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        db_event = fetch_stripe_event_by_id(event["id"])
        if not db_event:
            env = os.environ.get("ENVIRONMENT")
            ok_to_process_event = (event["livemode"] and env == "PROD") or (
                not event["livemode"] and env == "DEV"
            )
            if ok_to_process_event:
                process_event(event)
        return (
            jsonify({"success": True}),
            200,
        )  # Stripe just needs to see a 2xx status code
    except Exception as e:
        stack_trace = traceback.format_exc()
        try:
            error = f"Exception during Stripe webhook: {str(e)} {event}\n{stack_trace}"
        except:
            error = f"Exception during Stripe webhook: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/products", methods=["GET"])
def products():
    try:
        items = fetch_all_items()
        return jsonify(items), 200
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during fetching products: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500
