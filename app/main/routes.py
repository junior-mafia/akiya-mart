from app.main import bp
from flask import send_from_directory, current_app


@bp.route("/", defaults={"path": "index.html"})
@bp.route("/<path:path>")
def serve_static(path):
    return send_from_directory(current_app.static_folder, path)
