from app.main import bp
from flask import send_from_directory, current_app


@bp.route("/", defaults={"path": "index.html"})
@bp.route("/<path:path>")
def serve_static(path):
    return send_from_directory(current_app.static_folder, path)

# @bp.errorhandler(404)
# def page_not_found(e):
#     return send_from_directory(bp.static_folder, 'indexV2.html')


# @bp.route("/auth", defaults={"path": "auth.html"})
# def auth(path):
#     return send_from_directory(current_app.static_folder, path)

# Change /auth -> /#/auth


# @app.route("/payment/success")
# def payment_success():
#     # You can do any server-side processing you need here,
#     # such as recording the successful payment in your database.
    
#     # Then, you redirect the user to the relevant part of your React app.
#     return redirect("/#/payment-success")

# @app.route("/payment/cancel")
# def payment_cancel():
#     # Similarly, handle any necessary server-side logic here.

#     # Then, redirect the user back to your React app.
#     return redirect("/#/payment-cancel")