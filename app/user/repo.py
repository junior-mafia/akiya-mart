from app.extensions import db
from app.user.user import from_dict


def insert_user(user_data):
    try:
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
    users = db.metadata.tables["users"]
    stmt = users.select().where(users.c.email == email)
    result = db.session.execute(stmt).fetchone()
    if result is None:
        return None
    else:
        user = from_dict(result._asdict())
        return user


def fetch_user_by_id(user_id):
    users = db.metadata.tables["users"]
    stmt = users.select().where(users.c.user_id == user_id)
    result = db.session.execute(stmt).fetchone()
    if result is None:
        return None
    else:
        user = from_dict(result._asdict())
        return user


def fetch_user_by_stripe_customer_id(stripe_customer_id):
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
