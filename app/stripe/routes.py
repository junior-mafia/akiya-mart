from app.stripe import bp
from flask import request, jsonify, current_app as app
import stripe
import os
from flask_login import login_required, current_user
from app.stripe.repo import (
    fetch_stripe_event_by_id,
    create_subscription,
    fetch_prices_by_ids,
    insert_product,
    insert_price,
    update_product,
    update_price,
    delete_product,
    delete_price,
    fetch_all_items
)
from app.user.repo import fetch_user_by_id, fetch_user_by_stripe_customer_id
import traceback


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
        line_items = [{'price': price_id, 'quantity': 1} for price_id in price_ids]

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























# # The purpose of this method is just to create a subscription record
# # If the subscription record already exists, do nothing as some other process has already created it
# def handle_customer_subscription_created(event):
    # subscription = event["data"]["object"]
    # subscription_id = subscription["id"]
    # # We assume only 1 item per subscription
    # price_ids = [item["price"]["id"] for item in subscription["items"]["data"]]


#     customer_email = subscription["customer_email"]
#     user = fetch_user_by_email(customer_email)
#     subscription_record = {
#         "subscription_id": subscription_id,
#         "user_id": user.id,
#         "price_id": price_id,
#         "is_active": False,
#     }
#     create_subscription(subscription_record)


def handle_invoice_payment_succeeded(event):
    invoice_object = event['data']['object']
    customer_id = invoice_object['customer']
    user = fetch_user_by_stripe_customer_id(customer_id)
    line_items = invoice_object['lines']['data']
    
    subscription_records = set()
    subscription_item_records = []
    for line_item in line_items:
        if 'subscription' in line_item: # Could be items in the invoice that are NOT part of a subscription
            subscription_id = line_item['subscription']
            subscription_record = {
                "subscription_id": subscription_id,
                "user_id": user.id,
            }
            subscription_records.add(subscription_record)

            price_id = line_item['price']['id']
            subscription_item_record = {
                "subscription_id": subscription_id,
                "price_id": price_id,
            }
            subscription_item_records.append(subscription_item_record)
    
    create_subscription(event, subscription_records, subscription_item_records)


def handle_invoice_payment_failed(event):
    # Requires a subscription record
    # # Create if not exists
    # # # is_active=False
    # # # ON CONFLICT UPDATE is_active = False
    # Insert this (failed) invoice record
    # Transactional!
    pass


def handle_customer_subscription_deleted(event):
    # subscription = event["data"]["object"]
    # subscription_id = subscription["id"]
    # deactivate_subscription(subscription_id)
    pass








def handle_product_created(event):
    product_data = event["data"]["object"]
    product_record = {
        "product_id": product_data["id"],
        "name": product_data["name"],
        "description": product_data["description"],
    }
    insert_product(product_record)

def handle_product_updated(event):
    product_data = event["data"]["object"]
    product_record = {
        "product_id": product_data["id"],
        "name": product_data["name"],
        "description": product_data["description"],
    }
    update_product(product_record)

def handle_product_deleted(event):
    product_data = event["data"]["object"]
    product_id = product_data["id"]
    delete_product(product_id)

def handle_price_created(event):
    price_data = event["data"]["object"]
    recurring = price_data.get('recurring', {})
    price_record = {
        "price_id": price_data["id"],
        "product_id": price_data["product"],
        "currency": price_data["currency"],
        "unit_amount": price_data["unit_amount"],
        "recurring_interval": recurring.get('interval') if recurring else None,
    }
    insert_price(price_record)

def handle_price_updated(event):
    price_data = event["data"]["object"]
    recurring = price_data.get('recurring', {})
    price_record = {
        "price_id": price_data["id"],
        "product_id": price_data["product"],
        "currency": price_data["currency"],
        "unit_amount": price_data["unit_amount"],
        "recurring_interval": recurring.get('interval') if recurring else None,
    }
    update_price(price_record)

def handle_price_deleted(event):
    price_data = event["data"]["object"]
    price_id = price_data["id"]
    delete_price(price_id)

def process_event(event):
    event_type = event["type"]
    if event_type == "invoice.payment_succeeded":
        handle_invoice_payment_succeeded(event)
    elif event_type == "invoice.payment_failed":
        handle_invoice_payment_failed(event)
    elif event_type == "customer.subscription.deleted":
        handle_customer_subscription_deleted(event)
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
            ok_to_process_event = (event['livemode'] and env == 'PROD') or (not event['livemode'] and env == 'DEV')
            if ok_to_process_event:
                process_event(event)
        return jsonify({"success": True}), 200 # Stripe just needs to see a 2xx status code
    except Exception as e:
        try:
            error = f"Exception during Stripe webhook: {str(e)} {event}"
        except:
            error = f"Exception during Stripe webhook: {str(e)} "
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