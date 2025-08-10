from flask_jwt_extended import JWTManager
from src.web.routes import auth, user, chat, log, report

# Global JWT Manager instance
jwt = JWTManager()

def register_routes(app):
    """
    Registers all Flask blueprints and attaches JWT manager to app.
    """
    jwt.init_app(app)  # ✅ Do this first to avoid edge case errors

    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(log.bp)
    app.register_blueprint(report.bp)