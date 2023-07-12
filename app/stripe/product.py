from datetime import datetime
from app.extensions import db
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


def create_or_update_product(event):
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


def insert_or_update_product(event, product_record):
    try:
        with db.session.begin():
            products = db.metadata.tables["products"]
            stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]

            # Fetch existing record
            existing_record_stmt = select(products.c.updated_at).where(
                products.c.product_id == product_record["product_id"]
            )
            existing_record_result = db.session.execute(existing_record_stmt).fetchone()

            # Compare updated_at timestamp and proceed if the incoming data is fresher
            if (
                not existing_record_result
                or existing_record_result.updated_at < product_record["updated_at"]
            ):
                stmt1 = (
                    insert(products)
                    .values(product_record)
                    .on_conflict_do_update(
                        index_elements=["product_id"],
                        set_=dict(
                            internal_name=insert(products).excluded.internal_name,
                            name=insert(products).excluded.name,
                            description=insert(products).excluded.description,
                            active=insert(products).excluded.active,
                            updated_at=insert(products).excluded.updated_at,
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
