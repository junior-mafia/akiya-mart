from app.stripe.repo import insert_or_update_price
from datetime import datetime


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
        "active": price_data["active"],
        "created_at": event_timestamp,  # Will only get inserted on insert not on update
        "updated_at": event_timestamp,
    }
    insert_or_update_price(event, price_record)


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
        "active": price_data["active"],
        "created_at": event_timestamp,  # Will only get inserted on insert not on update
        "updated_at": event_timestamp,
    }
    insert_or_update_price(event, price_record)
