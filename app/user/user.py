class User:
    def __init__(
        self, user_id, email, hashed_password, stripe_customer_id, active, is_admin
    ):
        self.id = user_id
        self.email = email
        self.hashed_password = hashed_password
        self.active = active
        self.stripe_customer_id = stripe_customer_id
        self.is_admin = is_admin

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


def from_dict(user_dict):
    return User(
        user_id=user_dict["user_id"],
        email=user_dict["email"],
        hashed_password=user_dict["hashed_password"],
        stripe_customer_id=user_dict["stripe_customer_id"],
        active=True,  # Forced to have this field by flask-login
        is_admin=user_dict["is_admin"],
    )
