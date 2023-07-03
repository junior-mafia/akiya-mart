import re


class ValidationException(Exception):
    pass


def validate_email(email):
    if email is None:
        return False, "Missing email"
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email"
    return True, None


def validate_password(password):
    if password is None or len(password) < 8:
        return False, "Password must be at least 8 characters"
    return True, None


def validate_registration(email, password):
    validations = [
        validate_email(email),
        validate_password(password),
    ]
    are_all_valid = all([validation[0] for validation in validations])
    if not are_all_valid:
        error = [validation[1] for validation in validations if not validation[0]][0]
        raise ValidationException(error)


def validate_login(email, password):
    validations = [
        validate_email(email),
        validate_password(password),
    ]
    are_all_valid = all([validation[0] for validation in validations])
    if not are_all_valid:
        error = [validation[1] for validation in validations if not validation[0]][0]
        raise ValidationException(error)
