from app.extensions import db
from sqlalchemy import select


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
            .where(products.c.active == True)
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
            .where(subscriptions.c.status != "canceled")
        )
        result = db.session.execute(stmt).fetchone()
        if result is None:
            return None
        else:
            return result._asdict()


def fetch_active_subscription(user_id):
    with db.session.begin():
        subscriptions = db.metadata.tables["subscriptions"]
        stmt = (
            select(subscriptions.c.subscription_id)
            .where(subscriptions.c.user_id == user_id)
            .where(subscriptions.c.status.in_(["active", "trialing"]))
        )
        result = db.session.execute(stmt).fetchone()
        if result is None:
            return None
        else:
            return result._asdict()
