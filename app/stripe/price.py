from datetime import datetime
from app.extensions import db
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


def create_or_update_price(event):
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


def insert_or_update_price(event, price_record):
    try:
        with db.session.begin():
            prices = db.metadata.tables["prices"]
            stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]

            # Fetch existing record
            existing_record_stmt = select(prices.c.updated_at).where(
                prices.c.price_id == price_record["price_id"]
            )
            existing_record_result = db.session.execute(existing_record_stmt).fetchone()

            # Compare updated_at timestamp and proceed if the incoming data is fresher
            if (
                not existing_record_result
                or existing_record_result.updated_at < price_record["updated_at"]
            ):
                stmt1 = (
                    insert(prices)
                    .values(price_record)
                    .on_conflict_do_update(
                        index_elements=["price_id"],
                        set_=dict(
                            currency=insert(prices).excluded.currency,
                            unit_amount=insert(prices).excluded.unit_amount,
                            recurring_interval=insert(
                                prices
                            ).excluded.recurring_interval,
                            product_id=insert(prices).excluded.product_id,
                            active=insert(prices).excluded.active,
                            updated_at=insert(prices).excluded.updated_at,
                        ),
                    )
                )
                db.session.execute(stmt1)

            stmt2 = stripe_webhook_events.insert().values(
                event_id=event["id"],
                event_type=event["type"],
            )  # Raise on duplicate event
            db.session.execute(stmt2)

            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
