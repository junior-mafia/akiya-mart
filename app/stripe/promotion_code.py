from datetime import datetime
from app.extensions import db
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


def create_or_update_promotion_code(event):
    event_timestamp = datetime.utcfromtimestamp(event["created"])
    promotion_code_data = event["data"]["object"]
    promotion_code_record = {
        "promotion_code_id": promotion_code_data["id"],
        "code": promotion_code_data["code"],
        "active": promotion_code_data["active"],
        "coupon_id": promotion_code_data["coupon"]["id"],
        "created_at": event_timestamp,  # Will only get inserted on insert not on update
        "updated_at": event_timestamp,
    }
    insert_or_update_promotion_code(event, promotion_code_record)


def insert_or_update_promotion_code(event, promotion_code_record):
    try:
        with db.session.begin():
            promotion_codes = db.metadata.tables["promotion_codes"]
            stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]

            # Fetch existing record
            existing_record_stmt = select(promotion_codes.c.updated_at).where(
                promotion_codes.c.promotion_code_id
                == promotion_code_record["promotion_code_id"]
            )
            existing_record_result = db.session.execute(existing_record_stmt).fetchone()

            # Compare updated_at timestamp and proceed if the incoming data is fresher
            if (
                not existing_record_result
                or existing_record_result.updated_at
                < promotion_code_record["updated_at"]
            ):
                stmt1 = (
                    insert(promotion_codes)
                    .values(promotion_code_record)
                    .on_conflict_do_update(
                        index_elements=["promotion_code_id"],
                        set_=dict(
                            code=insert(promotion_codes).excluded.code,
                            active=insert(promotion_codes).excluded.active,
                            coupon_id=insert(promotion_codes).excluded.coupon_id,
                            updated_at=insert(promotion_codes).excluded.updated_at,
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
