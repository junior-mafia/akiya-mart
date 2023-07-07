from app.extensions import db
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


def fetch_stripe_event_by_id(event_id):
    with db.session.begin():
        stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]
        stmt = stripe_webhook_events.select().where(
            stripe_webhook_events.c.event_id == event_id
        )
        result = db.session.execute(stmt).fetchone()
        return result


def fetch_prices_by_ids(price_ids):
    with db.session.begin():
        prices = db.metadata.tables["prices"]
        stmt = prices.select().where(prices.c.price_id.in_(price_ids))
        result = db.session.execute(stmt).fetchall()
        return result


def insert_or_update_product(event, product_record):
    try:
        with db.session.begin():
            products = db.metadata.tables["products"]
            stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]

            # Fetch existing subscription record
            existing_product_stmt = select(products.c.updated_at).where(
                products.c.product_id == product_record["product_id"]
            )
            existing_product_result = db.session.execute(
                existing_product_stmt
            ).fetchone()

            # Compare updated_at timestamp and proceed if the incoming data is fresher
            if (
                not existing_product_result
                or existing_product_result.updated_at < product_record["updated_at"]
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


def insert_or_update_price(event, price_record):
    try:
        with db.session.begin():
            prices = db.metadata.tables["prices"]
            stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]

            # Fetch existing subscription record
            existing_price_stmt = select(prices.c.updated_at).where(
                prices.c.price_id == price_record["price_id"]
            )
            existing_price_result = db.session.execute(existing_price_stmt).fetchone()

            # Compare updated_at timestamp and proceed if the incoming data is fresher
            if (
                not existing_price_result
                or existing_price_result.updated_at < price_record["updated_at"]
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


def insert_or_update_subscription(event, subscription_record):
    try:
        with db.session.begin():
            subscriptions = db.metadata.tables["subscriptions"]
            stripe_webhook_events = db.metadata.tables["stripe_webhook_events"]

            # Fetch existing subscription record
            existing_subscription_stmt = select(subscriptions.c.updated_at).where(
                subscriptions.c.subscription_id
                == subscription_record["subscription_id"]
            )
            existing_subscription_result = db.session.execute(
                existing_subscription_stmt
            ).fetchone()

            # Compare updated_at timestamp and proceed if the incoming data is fresher
            if (
                not existing_subscription_result
                or existing_subscription_result.updated_at
                < subscription_record["updated_at"]
            ):
                stmt1 = (
                    insert(subscriptions)
                    .values(subscription_record)
                    .on_conflict_do_update(
                        index_elements=["subscription_id"],
                        set_=dict(
                            status=insert(subscriptions).excluded.status,
                            updated_at=insert(subscriptions).excluded.updated_at,
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


def fetch_items_by_internal_name(internal_name):
    # Could be more than one if there are multiple prices
    with db.session.begin():
        products = db.metadata.tables["products"]
        prices = db.metadata.tables["prices"]
        stmt = (
            select(
                prices.c.price_id,
                prices.c.currency,
                prices.c.unit_amount,
                prices.c.recurring_interval,
                products.c.name,
                products.c.description,
            )
            .select_from(
                products.join(prices, products.c.product_id == prices.c.product_id)
            )
            .where(products.c.internal_name == internal_name)
            .order_by(prices.c.unit_amount)
        )
        results = db.session.execute(stmt).fetchall()
        return [result._asdict() for result in results]


def fetch_non_cancelled_subscription(user_id):
    with db.session.begin():
        subscriptions = db.metadata.tables["subscriptions"]
        stmt = (
            select(subscriptions.c.subscription_id)
            .where(subscriptions.c.user_id == user_id)
            .where(subscriptions.c.status != 'canceled')
        )
        result = db.session.execute(stmt).fetchone()
        if result is None:
            return None
        else:
            return result._asdict()