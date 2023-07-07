from app.user import bp
from flask import jsonify, current_app as app
from flask_login import login_required, current_user
from app.user.repo import fetch_dashboard_data
import traceback


@bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    try:
        results = fetch_dashboard_data(current_user.id)
        if results is None:
            raise Exception(f"User not found with id: {current_user.id}")

        return jsonify({"success": True, "results": results}), 200
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during fetching of data for user dashboard: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500
