from app.auth import bp
from app.auth.validators import validate_registration, validate_login, ValidationException
from app.auth.register import register_user
from app.auth.login import log_in_user, IncorrectPasswordException, EmailNotFoundException
from app.auth.logout import handle_logout
from flask import request, jsonify, current_app as app
from flask_login import login_required, current_user


@bp.route("/is-logged-in", methods=["GET"])
def is_logged_in():
    try:
        is_logged_in = current_user.is_authenticated
        result = {"is_logged_in": is_logged_in}
        return (
            jsonify({"success": True, "result": result}),
            200,
        )
    except Exception as e:
        error = f"Exception during check to see if a user is logged in: {str(e)}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        validate_registration(email, password)
        register_user(email, password)
        return jsonify({"success": True}), 201
    except ValidationException as e:
        error = f"ValidationException during user registration: {str(e)}"
        user_message = str(e)
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 400
    except Exception as e:
        error = f"Exception during user registration: {str(e)}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        validate_login(email, password)
        log_in_user(email, password)
        return jsonify({"success": True}), 200
    except ValidationException as e:
        error = f"ValidationException during user login: {str(e)}"
        user_message = str(e)
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 400
    except EmailNotFoundException as e:
        error = f"EmailNotFoundException during user login: {str(e)}"
        user_message = "Email not found"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 400
    except IncorrectPasswordException as e:
        error = f"IncorrectPasswordException during user login: {str(e)}"
        user_message = "Password is incorrect"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 400
    except Exception as e:
        error = f"Exception during user login: {str(e)}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    try:
        handle_logout()
        return jsonify({"success": True}), 200
    except Exception as e:
        error = f"Exception during user logout: {str(e)}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500
