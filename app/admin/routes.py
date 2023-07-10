from app.admin import bp
from flask import jsonify, current_app as app
from flask_login import current_user
import traceback
from datetime import datetime
from app.tasks.tasks import (
    # runtask_nifty_details,
    # runtask_athome_details,
    task_rundate,
    task_listings_athome,
    task_listings_nifty,
    # runtask_generate_geojson,
    # runtask_post_scrape_verification,
    # runtask_translate,
)

@bp.route("/rundate", methods=["POST"])
def rundate():
    try:
        if not current_user.is_admin:
            return jsonify({"success": False, "message": "Not authorized"}), 401
        task_rundate.delay()
        results = {"message": "Running task: rundate"}
        return jsonify({"success": True, "results": results}), 200
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
            return jsonify({"success": False, "message": "Not authorized"}), 401
        today = datetime.now().strftime("%Y-%m-%d")
        task_listings_athome.delay({"run_date": today})
        results = {"message": "Running task: listings-athome"}
        return jsonify({"success": True, "results": results}), 200
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
            return jsonify({"success": False, "message": "Not authorized"}), 401
        today = datetime.now().strftime("%Y-%m-%d")
        task_listings_nifty.delay({"run_date": today})
        results = {"message": "Running task: listings-nifty"}
        return jsonify({"success": True, "results": results}), 200
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during listings-nifty task: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500
    



# @app.route("/post-scrape-verification")
# def post_scrape_verification():
#     today = datetime.now().strftime("%Y-%m-%d")
#     runtask_post_scrape_verification.delay({"run_date": today})
#     return "Running task: post-scrape-verification"


# @app.route("/nifty-details")
# def nifty_details():
#     today = datetime.now().strftime("%Y-%m-%d")
#     runtask_nifty_details.delay({"run_date": today})
#     return "Running task: nifty-details"


# @app.route("/athome-details")
# def athome_details():
#     today = datetime.now().strftime("%Y-%m-%d")
#     runtask_athome_details.delay({"run_date": today})
#     return "Running task: athome-details"


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

