from app.stripe import bp
from flask import request, jsonify, current_app as app
import os
from flask_login import login_required, current_user
from app.stripe.repo import (
    fetch_stripe_event_by_id,
    fetch_items_by_internal_name,
    fetch_non_cancelled_subscription,
)
from app.user.repo import fetch_user_by_id
import traceback
from app.stripe.checkout_session import (
    create_stripe_checkout_session_for_subscription,
    validate_price_ids,
)
from app.stripe.webhook import (
    process_event,
    validate_stripe_event,
)
from app.stripe.subscription import (
    cancel_subscription,
)


STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


@bp.route("/create-checkout-session", methods=["POST"])
@login_required
def create_checkout_session():
    try:
        subscription_id = fetch_non_cancelled_subscription(current_user.id)
        if subscription_id:
            raise Exception(
                f"User already has a non-cancelled subscription. user: {current_user.id} {subscription_id}"
            )

        data = request.get_json()
        price_ids = data.get("priceIds")
        validate_price_ids(price_ids)
        line_items = [{"price": price_id, "quantity": 1} for price_id in price_ids]

        user = fetch_user_by_id(current_user.id)
        if user is None:
            raise Exception(f"User not found with id: {current_user.id}")

        url = create_stripe_checkout_session_for_subscription(line_items)
        result = {"url": url}
        return jsonify({"success": True, "result": result}), 200
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during creation of Stripe checkout session: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


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


@bp.route("/products/<internal_name>", methods=["GET"])
def products(internal_name):
    try:
        items = fetch_items_by_internal_name(internal_name)
        if not items:
            raise Exception(f"Zero items found with internal name: {internal_name}")
        result = {"items": items}
        return jsonify({"success": True, "result": result}), 200
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during fetching products: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/cancel", methods=["POST"])
def cancel():
    try:
        subscription = fetch_non_cancelled_subscription(current_user.id)
        if not subscription:
            raise Exception(
                f"User does not have a non-cancelled subscription. user: {current_user.id} {subscription['subscription_id']}"
            )
        cancel_subscription(subscription["subscription_id"])
        return jsonify({"success": True}), 200
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during cancelling subscription: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500
