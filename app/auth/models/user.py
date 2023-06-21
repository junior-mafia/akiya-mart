class User:
    def __init__(self, user_id, email, hashed_password, active):
        self.id = user_id
        self.email = email
        self.hashed_password = hashed_password
        self.active = active

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


def unsafe_from_dict(user_dict):
    return User(
        user_id=user_dict["user_id"],
        email=user_dict["email"],
        hashed_password=user_dict["hashed_password"],
        active=True,  # Forced to have this field by flask-login
    )
