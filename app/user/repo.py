from app.extensions import db
from app.user.user import from_dict
from sqlalchemy import select, case
from sqlalchemy.sql import null


def insert_user(user_data):
    try:
        with db.session.begin():
            users = db.metadata.tables["users"]
            stmt = users.insert().values(
                email=user_data["email"],
                hashed_password=user_data["hashed_password"],
                stripe_customer_id=user_data["stripe_customer_id"],
            )
            db.session.execute(stmt)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def fetch_user_by_email(email):
    with db.session.begin():
        users = db.metadata.tables["users"]
        stmt = users.select().where(users.c.email == email)
        result = db.session.execute(stmt).fetchone()
        if result is None:
            return None
        else:
            user = from_dict(result._asdict())
            return user


def fetch_user_by_id(user_id):
    with db.session.begin():
        users = db.metadata.tables["users"]
        stmt = users.select().where(users.c.user_id == user_id)
        result = db.session.execute(stmt).fetchone()
        if result is None:
            return None
        else:
            user = from_dict(result._asdict())
            return user


def fetch_user_by_stripe_customer_id(stripe_customer_id):
    with db.session.begin():
        users = db.metadata.tables["users"]
        stmt = users.select().where(users.c.stripe_customer_id == stripe_customer_id)
        result = db.session.execute(stmt).fetchone()
        if result is None:
            return None
        else:
            user = from_dict(result._asdict())
            return user


def update_last_logged_in_at(user_id):
    try:
        with db.session.begin():
            users = db.metadata.tables["users"]
            stmt = (
                users.update()
                .where(users.c.user_id == user_id)
                .values(last_login_at=db.func.now())
            )
            db.session.execute(stmt)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e


def fetch_dashboard_data(user_id):
    with db.session.begin():
        users = db.metadata.tables["users"]
        subscriptions = db.metadata.tables["subscriptions"]
        subscription_items = db.metadata.tables["subscription_items"]
        prices = db.metadata.tables["prices"]
        products = db.metadata.tables["products"]

        stmt = (
            select(
                users.c.email,
                subscriptions.c.subscription_id,
                products.c.name.label("product_name"),
                subscriptions.c.status,
                prices.c.currency,
                prices.c.unit_amount,
                prices.c.recurring_interval,
            )
            .select_from(
                users.outerjoin(
                    subscriptions, users.c.user_id == subscriptions.c.user_id
                )
                .join(
                    subscription_items,
                    subscriptions.c.subscription_id
                    == subscription_items.c.subscription_id,
                )
                .join(prices, subscription_items.c.price_id == prices.c.price_id)
                .join(products, products.c.product_id == prices.c.product_id)
            )
            .where(users.c.user_id == user_id)
        )

        result = db.session.execute(stmt).fetchone()
        if result is None:
            return None
        else:
            return result._asdict()


# def fetch_dashboard_data(user_id):
#     with db.session.begin():
#         users = db.metadata.tables["users"]
#         subscriptions = db.metadata.tables["subscriptions"]
#         stmt = (
#             select(
#                 users.c.email,
#                 case(
#                     (subscriptions.c.subscription_id == null(), "free"),
#                     else_="subscribed",
#                 ).label("subscription_type"),
#                 case(
#                     (subscriptions.c.subscription_id == null(), "active"),
#                     else_=subscriptions.c.status,
#                 ).label("subscription_status"),
#             )
#             .select_from(
#                 users.outerjoin(
#                     subscriptions, users.c.user_id == subscriptions.c.user_id
#                 )
#             )
#             .where(users.c.user_id == user_id)
#             .order_by(subscriptions.c.updated_at.desc())
#         )
#         result = db.session.execute(stmt).fetchone()
#         if result is None:
#             return None
#         else:
#             return result._asdict()
