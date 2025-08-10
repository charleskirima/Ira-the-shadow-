from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from src.web import register_routes
from src.database.db import init_db

# ─── Rate Limiter Setup ──────────────────────────────────────────────────────
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.DevConfig")

    # ─── Initialize Extensions ────────────────────────────────────────────────
    limiter.init_app(app)

    # ─── Rate Limit Error Handler ─────────────────────────────────────────────
    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({"msg": "Too many requests, slow down."}), 429

    # ─── Exempt Health Check from Limiting ────────────────────────────────────
    @limiter.request_filter
    def exempt_health_check():
        return request.path == "/health"

    # ─── Initialize Database & Routes ─────────────────────────────────────────
    init_db()
    register_routes(app)

    return app