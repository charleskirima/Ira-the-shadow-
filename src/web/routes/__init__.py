from flask import Blueprint

# ✅ Import existing route blueprints
from .auth import bp as auth_bp
from .chat import bp as chat_bp
from .logs import bp as logs_bp
from .push import bp as push_bp
from .reports import bp as reports_bp
from .billing import bp as billing_bp  # ✅ New: billing routes

def register_routes(app):
    """
    Registers all API route blueprints to the Flask app.
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(push_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(billing_bp)  # 🔥 Billing/payment API routes