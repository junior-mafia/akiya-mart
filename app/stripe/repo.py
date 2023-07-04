from app.extensions import db
from sqlalchemy import select


def fetch_stripe_event_by_id(event_id):
    stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]
    stmt = stripe_webhook_events.select().where(
        stripe_webhook_events.c.event_id == event_id
    )
    result = db.session.execute(stmt).fetchone()
    return result


def fetch_prices_by_ids(price_ids):
    prices = db.metadata.tables["prices"]
    stmt = prices.select().where(prices.c.price_id.in_(price_ids))
    result = db.session.execute(stmt).fetchall()
    return result


def insert_product(product_record):
    try:
        products = db.metadata.tables["products"]
        stmt = products.insert().values(
            product_id=product_record["product_id"],
            name=product_record["name"],
            description=product_record["description"],
            created_at=product_record["now"],
            updated_at=product_record["now"],
        )
        db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def update_product(product_record):
    try:
        products = db.metadata.tables["products"]
        stmt = (
            products.update()
            .where(products.c.product_id == product_record["product_id"])
            .values(
                name=product_record["name"],
                description=product_record["description"],
                updated_at=product_record["now"],
            )
        )
        db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def delete_product(product_id):
    try:
        products = db.metadata.tables["products"]
        stmt = products.delete().where(products.c.product_id == product_id)
        db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def insert_price(price_record):
    try:
        prices = db.metadata.tables["prices"]
        stmt = prices.insert().values(
            price_id=price_record["price_id"],
            product_id=price_record["product_id"],
            unit_amount=price_record["unit_amount"],
            recurring_interval=price_record["recurring_interval"],
            currency=price_record["currency"],
            created_at=price_record["now"],
            updated_at=price_record["now"],
        )
        db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def update_price(price_record):
    try:
        prices = db.metadata.tables["prices"]
        stmt = (
            prices.update()
            .where(prices.c.price_id == price_record["price_id"])
            .values(
                currency=price_record["currency"],
                unit_amount=price_record["unit_amount"],
                recurring_interval=price_record["recurring_interval"],
                product_id=price_record["product_id"],
                updated_at=price_record["now"],
            )
        )
        db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def delete_price(price_id):
    try:
        prices = db.metadata.tables["prices"]
        stmt = prices.delete().where(prices.c.price_id == price_id)
        db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def create_subscription(event, subscriptions_records, subscription_items_records):
    try:
        with db.session.begin():
            subscriptions = db.metadata.tables["subscriptions"]
            subscription_items = db.metadata.tables["subscription_items"]
            stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]

            stmt1 = (
                subscriptions.insert()
                .values(subscriptions_records)
            )
            db.session.execute(stmt1)

            stmt2 = (
                subscription_items.insert()
                .values(subscription_items_records)
            )
            db.session.execute(stmt2)

            stmt3 = (
                stripe_webhook_events.insert()
                .values(
                    event_id=event["id"],
                    event_type=event["type"],
                )
            )
            db.session.execute(stmt3)

            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def insert_or_update_invoice(event, invoice_record):
    try:
        with db.session.begin():
            invoices = db.metadata.tables["invoices"]
            stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]

            stmt1 = invoices.insert().values(invoice_record)
            stmt1 = stmt1.on_conflict_do_update(
                index_elements=['invoice_id'],
                condition=(
                    invoices.c.updated_at < invoice_record['updated_at']
                ),
                set_=dict(
                    amount_paid=stmt1.excluded.amount_paid,
                    updated_at=db.func.now()
                )
            )
            db.session.execute(stmt1)

            stmt2 = (
                stripe_webhook_events.insert()
                .values(
                    event_id=event["id"],
                    event_type=event["type"],
                )
            )
            db.session.execute(stmt2)

            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def fetch_all_items():
    products = db.metadata.tables["products"]
    prices = db.metadata.tables["prices"]
    stmt = select(
        prices.c.price_id, prices.c.unit_amount, products.c.name, products.c.description
    ).select_from(products.join(prices, products.c.product_id == prices.c.product_id))
    result = db.session.execute(stmt).fetchall()
    return [row._asdict() for row in result]


# def deactivate_subscription(event, subscription_id):
#     try:
#         with db.session.begin():
#             now = db.func.now()
#             stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]
#             stmt1 = (
#                 stripe_webhook_events.insert()
#                 .values(
#                     event_id=event["id"],
#                     event_type=event["type"],
#                     created_at=now,
#                 )
#                 .on_conflict_do_nothing()
#             )
#             db.session.execute(stmt1)

#             subscriptions = db.metadata.tables["subscriptions"]
#             now = db.func.now()
#             stmt2 = (
#                 subscriptions.update()
#                 .where(subscriptions.c.subscription_id == subscription_id)
#                 .values(
#                     is_active=False,
#                     cancelled_at=now,
#                     updated_at=now,
#                 )
#             )
#             db.session.execute(stmt2)
#             db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         error = f"Failed to deactivate subscription: {str(e)}"
#         raise InsertSubscriptionError(error)
