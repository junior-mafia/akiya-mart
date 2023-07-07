from app.listings import bp
from app.listings.repo import fetch_listing_by_id
from flask import jsonify, current_app as app
import traceback


@bp.route("/<source>/<bukken_id>", methods=["GET"])
def active_subscription(source, bukken_id):
    try:
        results = fetch_listing_by_id(source, bukken_id)
        return jsonify({"success": True, "results": results}), 200
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = (
            f"Exception during fetching active subscription: {str(e)}\n{stack_trace}"
        )
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500
