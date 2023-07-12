from datetime import datetime
from app.extensions import db
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


def create_or_update_coupon(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    coupon_data = event["data"]["object"]
    coupon_record = {
        "coupon_id": coupon_data["id"],
        "name": coupon_data["name"],
        "valid": coupon_data["valid"],
        "currency": coupon_data["currency"],
        "amount_off": coupon_data["amount_off"],
        "percent_off": coupon_data["percent_off"],
        "duration": coupon_data["duration"],
        "duration_in_months": coupon_data["duration_in_months"],
        "created_at": event_timestamp,  # Will only get inserted on insert not on update
        "updated_at": event_timestamp,
    }
    insert_or_update_coupon(event, coupon_record)


def insert_or_update_coupon(event, coupon_record):
    try:
        with db.session.begin():
            coupons = db.metadata.tables["coupons"]
            stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]

            # Fetch existing record
            existing_record_stmt = select(coupons.c.updated_at).where(
                coupons.c.coupon_id == coupon_record["coupon_id"]
            )
            existing_record_result = db.session.execute(existing_record_stmt).fetchone()

            # Compare updated_at timestamp and proceed if the incoming data is fresher
            if (
                not existing_record_result
                or existing_record_result.updated_at < coupon_record["updated_at"]
            ):
                stmt1 = (
                    insert(coupons)
                    .values(coupon_record)
                    .on_conflict_do_update(
                        index_elements=["coupon_id"],
                        set_=dict(
                            name=insert(coupons).excluded.name,
                            valid=insert(coupons).excluded.valid,
                            currency=insert(coupons).excluded.currency,
                            amount_off=insert(coupons).excluded.amount_off,
                            percent_off=insert(coupons).excluded.percent_off,
                            duration=insert(coupons).excluded.duration,
                            duration_in_months=insert(
                                coupons
                            ).excluded.duration_in_months,
                            updated_at=insert(coupons).excluded.updated_at,
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
