from app.auth import bp
from app.auth.validators import validate_registration, validate_login
from app.auth.register import handle_register
from app.auth.login import handle_login
from app.auth.logout import handle_logout
from flask import request, jsonify
from flask_login import login_required, current_user


@bp.route("/is-logged-in", methods=["GET"])
def is_logged_in():
    return jsonify({"is_logged_in": current_user.is_authenticated}), 200


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    _, error = validate_registration(email, password)
    if error:
        return jsonify({"error": "Bad Request", "message": error}), 400

    _, error = handle_register(email, password)
    if error:
        return jsonify({"error": "Internal Server Error", "message": error}), 500

    return jsonify({"message": "User registered successfully"}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    _, error = validate_login(email, password)
    if error:
        return jsonify({"error": "Bad Request", "message": error}), 400

    _, error = handle_login(email, password)
    if error:
        return jsonify({"error": "Internal Server Error", "message": error}), 500

    return jsonify({"message": "User logged in successfully"}), 200


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    _, error = handle_logout()
    if error:
        return jsonify({"error": "Internal Server Error", "message": error}), 500

    return jsonify({"message": "User logged out successfully"}), 200
