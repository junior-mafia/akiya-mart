from app.user.repo import fetch_user_by_stripe_customer_id
from datetime import datetime
import os
import stripe
from app.extensions import db
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

# If the subscription status is active or trialing, then you can grant access.
# If the subscription status is past_due, unpaid, canceled, or incomplete, then you can deny access.


def create_customer_subscription(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    subscription = event["data"]["object"]
    subscription_id = subscription["id"]
    customer_id = subscription["customer"]
    user = fetch_user_by_stripe_customer_id(customer_id)
    status = subscription["status"]
    discount = subscription.get("discount")
    if discount:
        promotion_code_id = discount["promotion_code"]
    else:
        promotion_code_id = None
    subscription_record = {
        "subscription_id": subscription_id,
        "user_id": user.id,
        "status": status,
        "promotion_code_id": promotion_code_id,
        "created_at": event_timestamp,  # Will only get inserted on insert not on update
        "updated_at": event_timestamp,
    }

    # At the moment there is only one item per subscription
    line_items = subscription["items"]["data"]
    subscription_item_records = []
    for line_item in line_items:
        price_id = line_item["price"]["id"]
        subscription_item_record = {
            "subscription_item_id": line_item["id"],
            "subscription_id": subscription_id,
            "price_id": price_id,
            "created_at": event_timestamp,
            "updated_at": event_timestamp,
            "deleted_at": None,
        }
        subscription_item_records.append(subscription_item_record)

    insert_or_update_subscription(event, subscription_record, subscription_item_records)


def update_customer_subscription(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    subscription = event["data"]["object"]
    subscription_id = subscription["id"]
    customer_id = subscription["customer"]
    user = fetch_user_by_stripe_customer_id(customer_id)
    status = subscription["status"]
    subscription_record = {
        "subscription_id": subscription_id,
        "user_id": user.id,
        "status": status,
        "created_at": event_timestamp,  # Will only get inserted on insert not on update
        "updated_at": event_timestamp,
    }
    insert_or_update_subscription(event, subscription_record)


def cancel_customer_subscription(subscription_id):
    stripe.api_key = STRIPE_SECRET_KEY
    stripe.Subscription.delete(subscription_id)


def insert_or_update_subscription(
    event, subscription_record, subscription_item_records=None
):
    try:
        with db.session.begin():
            subscriptions = db.metadata.tables["subscriptions"]
            subscription_items = db.metadata.tables["subscription_items"]
            stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]

            # Fetch existing record
            existing_record_stmt = select(subscriptions.c.updated_at).where(
                subscriptions.c.subscription_id
                == subscription_record["subscription_id"]
            )
            existing_record_result = db.session.execute(existing_record_stmt).fetchone()

            # Compare updated_at timestamp and proceed if the incoming data is fresher
            if (
                not existing_record_result
                or existing_record_result.updated_at < subscription_record["updated_at"]
            ):
                stmt1 = (
                    insert(subscriptions)
                    .values(subscription_record)
                    .on_conflict_do_update(
                        index_elements=["subscription_id"],
                        set_=dict(
                            user_id=insert(subscriptions).excluded.user_id,
                            status=insert(subscriptions).excluded.status,
                            promotion_code_id=insert(
                                subscriptions
                            ).excluded.promotion_code_id,
                            updated_at=insert(subscriptions).excluded.updated_at,
                        ),
                    )
                )
                db.session.execute(stmt1)

            if subscription_item_records:
                stmt2 = (
                    insert(subscription_items)
                    .values(subscription_item_records)
                    .on_conflict_do_nothing()
                )
                db.session.execute(stmt2)

            stmt3 = stripe_webhook_events.insert().values(
                event_id=event["id"],
                event_type=event["type"],
            )  # Raise on duplicate event
            db.session.execute(stmt3)

            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


# {
#   "api_version": "2022-11-15",
#   "created": 1688858082,
#   "data": {
#     "object": {
#       "application": null,
#       "application_fee_percent": null,
#       "automatic_tax": {
#         "enabled": false
#       },
#       "billing_cycle_anchor": 1688858082,
#       "billing_thresholds": null,
#       "cancel_at": null,
#       "cancel_at_period_end": false,
#       "canceled_at": null,
#       "cancellation_details": {
#         "comment": null,
#         "feedback": null,
#         "reason": null
#       },
#       "collection_method": "charge_automatically",
#       "created": 1688858082,
#       "currency": "usd",
#       "current_period_end": 1691536482,
#       "current_period_start": 1688858082,
#       "customer": "cus_OD0asY7HhSCtQL",
#       "days_until_due": null,
#       "default_payment_method": "pm_1NQaeUCvWkOgLnHEYkMQGsoE",
#       "default_source": null,
#       "default_tax_rates": [],
#       "description": null,
#       "discount": {
#         "checkout_session": null,
#         "coupon": {
#           "amount_off": null,
#           "created": 1688857921,
#           "currency": null,
#           "duration": "forever",
#           "duration_in_months": null,
#           "id": "9aZ03e2b",
#           "livemode": false,
#           "max_redemptions": null,
#           "metadata": {},
#           "name": "ADMIN",
#           "object": "coupon",
#           "percent_off": 100.0,
#           "redeem_by": null,
#           "times_redeemed": 1,
#           "valid": true
#         },
#         "customer": "cus_OD0asY7HhSCtQL",
#         "end": null,
#         "id": "di_1NRkKsCvWkOgLnHEutMmz70N",
#         "invoice": null,
#         "invoice_item": null,
#         "object": "discount",
#         "promotion_code": "promo_1NRkIHCvWkOgLnHEaXRVtyDL",
#         "start": 1688858082,
#         "subscription": "sub_1NRkKsCvWkOgLnHExDYvjRVh"
#       },
#       "ended_at": null,
#       "id": "sub_1NRkKsCvWkOgLnHExDYvjRVh",
#       "items": {
#         "data": [
#           {
#             "billing_thresholds": null,
#             "created": 1688858082,
#             "id": "si_OECkmBzhR5SsTk",
#             "metadata": {},
#             "object": "subscription_item",
#             "plan": {
#               "active": true,
#               "aggregate_usage": null,
#               "amount": 1500,
#               "amount_decimal": "1500",
#               "billing_scheme": "per_unit",
#               "created": 1688681655,
#               "currency": "usd",
#               "id": "price_1NR0RHCvWkOgLnHExoUhTF1m",
#               "interval": "month",
#               "interval_count": 1,
#               "livemode": false,
#               "metadata": {},
#               "nickname": null,
#               "object": "plan",
#               "product": "prod_ODRJ3Gatj4sGC3",
#               "tiers_mode": null,
#               "transform_usage": null,
#               "trial_period_days": null,
#               "usage_type": "licensed"
#             },
#             "price": {
#               "active": true,
#               "billing_scheme": "per_unit",
#               "created": 1688681655,
#               "currency": "usd",
#               "custom_unit_amount": null,
#               "id": "price_1NR0RHCvWkOgLnHExoUhTF1m",
#               "livemode": false,
#               "lookup_key": null,
#               "metadata": {},
#               "nickname": null,
#               "object": "price",
#               "product": "prod_ODRJ3Gatj4sGC3",
#               "recurring": {
#                 "aggregate_usage": null,
#                 "interval": "month",
#                 "interval_count": 1,
#                 "trial_period_days": null,
#                 "usage_type": "licensed"
#               },
#               "tax_behavior": "unspecified",
#               "tiers_mode": null,
#               "transform_quantity": null,
#               "type": "recurring",
#               "unit_amount": 1500,
#               "unit_amount_decimal": "1500"
#             },
#             "quantity": 1,
#             "subscription": "sub_1NRkKsCvWkOgLnHExDYvjRVh",
#             "tax_rates": []
#           }
#         ],
#         "has_more": false,
#         "object": "list",
#         "total_count": 1,
#         "url": "/v1/subscription_items?subscription=sub_1NRkKsCvWkOgLnHExDYvjRVh"
#       },
#       "latest_invoice": "in_1NRkKsCvWkOgLnHExa84KSKc",
#       "livemode": false,
#       "metadata": {},
#       "next_pending_invoice_item_invoice": null,
#       "object": "subscription",
#       "on_behalf_of": null,
#       "pause_collection": null,
#       "payment_settings": {
#         "payment_method_options": null,
#         "payment_method_types": null,
#         "save_default_payment_method": "off"
#       },
#       "pending_invoice_item_interval": null,
#       "pending_setup_intent": null,
#       "pending_update": null,
#       "plan": {
#         "active": true,
#         "aggregate_usage": null,
#         "amount": 1500,
#         "amount_decimal": "1500",
#         "billing_scheme": "per_unit",
#         "created": 1688681655,
#         "currency": "usd",
#         "id": "price_1NR0RHCvWkOgLnHExoUhTF1m",
#         "interval": "month",
#         "interval_count": 1,
#         "livemode": false,
#         "metadata": {},
#         "nickname": null,
#         "object": "plan",
#         "product": "prod_ODRJ3Gatj4sGC3",
#         "tiers_mode": null,
#         "transform_usage": null,
#         "trial_period_days": null,
#         "usage_type": "licensed"
#       },
#       "quantity": 1,
#       "schedule": null,
#       "start_date": 1688858082,
#       "status": "active",
#       "test_clock": null,
#       "transfer_data": null,
#       "trial_end": null,
#       "trial_settings": {
#         "end_behavior": {
#           "missing_payment_method": "create_invoice"
#         }
#       },
#       "trial_start": null
#     }
#   },
#   "id": "evt_1NRkKuCvWkOgLnHEUqQiBNel",
#   "livemode": false,
#   "object": "event",
#   "pending_webhooks": 3,
#   "request": {
#     "id": null,
#     "idempotency_key": null
#   },
#   "type": "customer.subscription.created"
# }
