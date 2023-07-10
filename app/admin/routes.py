from app.admin import bp
from flask import jsonify, current_app as app
from flask_login import current_user
import traceback
from datetime import datetime
from app.tasks.tasks import (
    task_rundate,
    task_listings_athome,
    task_listings_nifty,
    task_listings_details_athome,
    task_listings_details_nifty,
    task_listings_details_translate,
    task_generate_geojson_task,
    generate_task_run_all,
)


class UnauthorizedError(Exception):
    pass


@bp.route("/rundate", methods=["POST"])
def rundate():
    try:
        if not current_user.is_admin:
            raise UnauthorizedError("Not authorized")

        task_rundate.delay()
        results = {"message": "Running task: rundate"}

        return jsonify({"success": True, "results": results}), 200
    except UnauthorizedError as e:
        error = f"UnauthorizedError during access to admin dashboard: {str(e)}"
        user_message = "Unauthorized access"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 401
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during rundate task: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/listings-athome", methods=["POST"])
def listings_athome():
    try:
        if not current_user.is_admin:
            raise UnauthorizedError("Not authorized")

        today = datetime.now().strftime("%Y-%m-%d")
        task_listings_athome.delay({"run_date": today})
        results = {"message": "Running task: listings-athome"}

        return jsonify({"success": True, "results": results}), 200
    except UnauthorizedError as e:
        error = f"UnauthorizedError during access to admin dashboard: {str(e)}"
        user_message = "Unauthorized access"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 401
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during listings-athome task: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/listings-nifty", methods=["POST"])
def listings_nifty():
    try:
        if not current_user.is_admin:
            raise UnauthorizedError("Not authorized")

        today = datetime.now().strftime("%Y-%m-%d")
        task_listings_nifty.delay({"run_date": today})
        results = {"message": "Running task: listings-nifty"}

        return jsonify({"success": True, "results": results}), 200
    except UnauthorizedError as e:
        error = f"UnauthorizedError during access to admin dashboard: {str(e)}"
        user_message = "Unauthorized access"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 401
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during listings-nifty task: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/listings-details-athome", methods=["POST"])
def listings_details_athome():
    try:
        if not current_user.is_admin:
            raise UnauthorizedError("Not authorized")

        today = datetime.now().strftime("%Y-%m-%d")
        task_listings_details_athome.delay({"run_date": today})
        results = {"message": "Running task: listings-details-athome"}

        return jsonify({"success": True, "results": results}), 200
    except UnauthorizedError as e:
        error = f"UnauthorizedError during access to admin dashboard: {str(e)}"
        user_message = "Unauthorized access"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 401
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = (
            f"Exception during listings-details-athome task: {str(e)}\n{stack_trace}"
        )
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/listings-details-nifty", methods=["POST"])
def listings_details_nifty():
    try:
        if not current_user.is_admin:
            raise UnauthorizedError("Not authorized")

        today = datetime.now().strftime("%Y-%m-%d")
        task_listings_details_nifty.delay({"run_date": today})
        results = {"message": "Running task: listings-details-nifty"}

        return jsonify({"success": True, "results": results}), 200
    except UnauthorizedError as e:
        error = f"UnauthorizedError during access to admin dashboard: {str(e)}"
        user_message = "Unauthorized access"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 401
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during listings-details-nifty task: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/listings-details-translate", methods=["POST"])
def listings_details_translate():
    try:
        if not current_user.is_admin:
            raise UnauthorizedError("Not authorized")

        today = datetime.now().strftime("%Y-%m-%d")
        task_listings_details_translate.delay({"run_date": today})
        results = {"message": "Running task: listings-details-translate"}

        return jsonify({"success": True, "results": results}), 200
    except UnauthorizedError as e:
        error = f"UnauthorizedError during access to admin dashboard: {str(e)}"
        user_message = "Unauthorized access"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 401
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = (
            f"Exception during listings-details-translate task: {str(e)}\n{stack_trace}"
        )
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("/generate-geojson", methods=["POST"])
def generate_geojson():
    try:
        if not current_user.is_admin:
            raise UnauthorizedError("Not authorized")

        today = datetime.now().strftime("%Y-%m-%d")
        task_generate_geojson_task.delay({"run_date": today})
        results = {"message": "Running task: generate-geojson"}

        return jsonify({"success": True, "results": results}), 200
    except UnauthorizedError as e:
        error = f"UnauthorizedError during access to admin dashboard: {str(e)}"
        user_message = "Unauthorized access"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 401
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during generate-geojson task: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500


@bp.route("run-all", methods=["GET"])
def runall():
    try:
        if not current_user.is_admin:
            raise UnauthorizedError("Not authorized")

        run_all = generate_task_run_all()
        run_all.apply_async()
        results = {"message": "Running task: run-all"}

        return jsonify({"success": True, "results": results}), 200
    except UnauthorizedError as e:
        error = f"UnauthorizedError during access to admin dashboard: {str(e)}"
        user_message = "Unauthorized access"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 401
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during run-all task: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500
