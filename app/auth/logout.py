from flask_login import logout_user


def handle_logout():
    logout_user()
    return None, None
