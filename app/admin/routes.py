from app.admin import bp
from flask import jsonify, current_app as app
from flask_login import login_required, current_user
import traceback


@bp.route("/fetch-admin-data", methods=["GET"])
@login_required
def fetch_admin_data():
    try:
        if not current_user.is_admin:
            return jsonify({"success": False, "message": "Not authorized"}), 401
        results = {"message": "This is the admin dashboard"}
        return jsonify({"success": True, "results": results}), 200
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during loading admin dashboard: {str(e)}\n{stack_trace}"
        user_message = "Oops something went wrong"
        app.logger.error(error)
        return jsonify({"success": False, "message": user_message}), 500
