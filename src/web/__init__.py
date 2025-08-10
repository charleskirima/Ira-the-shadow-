from flask import Flask
from src.web import register_routes
from src.database.db import init_db

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load default configuration
    app.config.from_object("config.DevConfig")

    # Optional override via environment (e.g. production)
    # app.config.from_envvar("APP_CONFIG_FILE", silent=True)

    # Initialize extensions, e.g. database
    init_db()

    # Register routes/blueprints
    register_routes(app)

    return app