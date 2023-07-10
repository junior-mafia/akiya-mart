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
    # runtask_generate_geojson,
    # runtask_post_scrape_verification,
    # runtask_translate,
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
        error = f"Exception during listings-details-athome task: {str(e)}\n{stack_trace}"
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

















# @app.route("/translate")
# def translate():
#     today = datetime.now().strftime("%Y-%m-%d")
#     runtask_translate.delay({"run_date": today})
#     return "Running task: translate"


# @app.route("/generate-geojson")
# def generate_geojson():
#     today = datetime.now().strftime("%Y-%m-%d")
#     runtask_generate_geojson.delay({"run_date": today})
#     return "Running task: generate-geojson"


# @app.route("/run-from-details")
# def run_from_details():
#     today = datetime.now().strftime("%Y-%m-%d")
#     scrape_listings_details = chain(
#         runtask_nifty_details.s(today),
#         runtask_athome_details.s(),
#     )
#     translate = chain(runtask_translate.s())
#     generate_geojson = chain(runtask_generate_geojson.s())
#     chained_task = chain(
#         scrape_listings_details,
#         translate,
#         generate_geojson,
#     )
#     chained_task.apply_async()
#     return "Running task: run-from-details"


# @app.route("/runall")
# def runall():
#     insert_rundate = chain(runtask_insert_rundate.s())
#     scrape_listings = chain(
#         runtask_nifty.s(),
#         runtask_athome.s(),
#     )
#     verify_listings_post_scrape = chain(runtask_post_scrape_verification.s())
#     scrape_listings_details = chain(
#         runtask_nifty_details.s(),
#         runtask_athome_details.s(),
#     )
#     translate = chain(runtask_translate.s())
#     generate_geojson = chain(runtask_generate_geojson.s())
#     chained_task = chain(
#         insert_rundate,
#         scrape_listings,
#         verify_listings_post_scrape,
#         scrape_listings_details,
#         translate,
#         generate_geojson,
#     )
#     chained_task.apply_async()
#     return "Running task: runall"

