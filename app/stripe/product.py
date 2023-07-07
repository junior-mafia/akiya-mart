from app.stripe.repo import insert_or_update_product
from datetime import datetime


def handle_product_created(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    product_data = event["data"]["object"]
    product_record = {
        "product_id": product_data["id"],
        "internal_name": product_data["metadata"].get("internal_name"),
        "name": product_data["name"],
        "description": product_data["description"],
        "active": product_data["active"],
        "created_at": event_timestamp,  # Will only get inserted on insert not on update
        "updated_at": event_timestamp,
    }
    insert_or_update_product(event, product_record)


def handle_product_updated(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    product_data = event["data"]["object"]
    product_record = {
        "product_id": product_data["id"],
        "internal_name": product_data["metadata"].get("internal_name"),
        "name": product_data["name"],
        "description": product_data["description"],
        "active": product_data["active"],
        "created_at": event_timestamp,  # Will only get inserted on insert not on update
        "updated_at": event_timestamp,
    }
    insert_or_update_product(event, product_record)
