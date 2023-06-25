from app.stripe import bp
from flask import request, jsonify
import stripe
import os
from flask_login import login_required, current_user


SERVER_URL = os.environ.get("SERVER_URL")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

store_items = {
    "PREMIUM": {"price": "price_1NMWZLCvWkOgLnHEYLoPXwYl", "quantity": 1},
}


class InvalidProductIdError(Exception):
    pass


@bp.route("/create-checkout-session", methods=["POST"])
@login_required
def create_checkout_session():
    try:
        data = request.get_json()
        product_id = data.get("productId")
        line_item = store_items.get(product_id)
        if not line_item:
            raise InvalidProductIdError("Invalid product_id")

        stripe.api_key = STRIPE_SECRET_KEY
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            success_url=f"{SERVER_URL}/#/success",
            cancel_url=f"{SERVER_URL}/#/cancel",
            line_items=[line_item],
            customer_email=current_user.email,
            allow_promotion_codes=True,
        )
        return jsonify({"url": checkout_session.url}), 201
    except InvalidProductIdError as e:
        return jsonify({"message": "InvalidProductIdError", "details": str(e)}), 400
    except stripe.error.StripeError as e:
        return (
            jsonify(
                {
                    "message": "Failed to create Stripe checkout session",
                    "details": str(e),
                }
            ),
            500,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "Internal server error",
                    "details": str(e),
                }
            ),
            500,
        )
