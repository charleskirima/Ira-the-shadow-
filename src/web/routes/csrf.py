from flask import Blueprint, jsonify
from flask_wtf.csrf import generate_csrf

bp = Blueprint("csrf", __name__, url_prefix="/csrf")

@bp.route("/token", methods=["GET"])
def get_csrf_token():
    """
    Returns a CSRF token for use in frontend forms or API headers.
    """
    try:
        token = generate_csrf()
        return jsonify({"csrf_token": token}), 200
    except Exception as e:
        print(f"[❌] Failed to generate CSRF token: {e}")
        return jsonify({"error": "Could not generate CSRF token"}), 500