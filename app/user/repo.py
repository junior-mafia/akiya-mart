from app.extensions import db
from app.user.user import from_dict
from sqlalchemy import select
from sqlalchemy import cast, Integer


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
        promotion_codes = db.metadata.tables["promotion_codes"]
        coupons = db.metadata.tables["coupons"]

        stmt = (
            select(
                users.c.email,
                users.c.is_admin,
                subscriptions.c.subscription_id,
                products.c.name.label("product_name"),
                subscriptions.c.status,
                prices.c.currency,
                prices.c.unit_amount,
                prices.c.recurring_interval,
                promotion_codes.c.code.label("promotion_code"),
                cast(coupons.c.percent_off, Integer),
                cast(coupons.c.amount_off, Integer),
                coupons.c.currency.label("coupon_currency"),
                coupons.c.duration,
                coupons.c.duration_in_months,
            )
            .select_from(
                users.outerjoin(
                    subscriptions, users.c.user_id == subscriptions.c.user_id
                )
                .outerjoin(
                    subscription_items,
                    subscriptions.c.subscription_id
                    == subscription_items.c.subscription_id,
                )
                .outerjoin(prices, subscription_items.c.price_id == prices.c.price_id)
                .outerjoin(products, products.c.product_id == prices.c.product_id)
                .outerjoin(
                    promotion_codes,
                    subscriptions.c.promotion_code_id
                    == promotion_codes.c.promotion_code_id,
                )
                .outerjoin(coupons, promotion_codes.c.coupon_id == coupons.c.coupon_id)
            )
            .where(users.c.user_id == user_id)
            .order_by(subscriptions.c.created_at.desc())
        )

        result = db.session.execute(stmt).fetchone()
        if result is None:
            return None
        else:
            return result._asdict()
