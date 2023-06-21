from app.extensions import db
from sqlalchemy.exc import IntegrityError
from app.auth.models.user import unsafe_from_dict


def insert_user(user):
    users = db.metadata.tables["users"]
    stmt = users.insert().values(
        email=user["email"], hashed_password=user["hashed_password"]
    )

    try:
        db.session.execute(stmt)
        db.session.commit()
        return None, None
    except IntegrityError:
        db.session.rollback()
        return None, "This email is already registered"


def fetch_user_by_email(email):
    users = db.metadata.tables["users"]

    try:
        stmt = users.select().where(users.c.email == email)
        result = db.session.execute(stmt).fetchone()
    except Exception as e:
        return None, str(e)

    if result is None:
        return None, None
    else:
        user_dict = result._asdict()
        user = unsafe_from_dict(user_dict)
        return user, None


def fetch_user_by_id(user_id):
    users = db.metadata.tables["users"]

    try:
        stmt = users.select().where(users.c.user_id == user_id)
        result = db.session.execute(stmt).fetchone()
    except Exception as e:
        return None, str(e)

    if result is None:
        return None, None
    else:
        user_dict = result._asdict()
        user = unsafe_from_dict(user_dict)
        return user, None
