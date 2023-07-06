from app.stripe.repo import (
    insert_or_update_subscription,
)
from app.user.repo import fetch_user_by_stripe_customer_id
from datetime import datetime


# If the subscription status is active or trialing, then you can grant access.
# If the subscription status is past_due, unpaid, canceled, or incomplete, then you can deny access.


def handle_customer_subscription_created(event):
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

    # line_items = subscription["items"]["data"]
    # subscription_item_records = []
    # for line_item in line_items:
    #     price_id = line_item["price"]["id"]
    #     subscription_item_record = {
    #         "subscription_id": subscription_id,
    #         "price_id": price_id,
    #         "created_at": event_timestamp,
    #         "updated_at": event_timestamp,
    #     }
    #     subscription_item_records.append(subscription_item_record)

    # create_subscription(event, subscription_record, subscription_item_records)


def handle_customer_subscription_updated(event):
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
