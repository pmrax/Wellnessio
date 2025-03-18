from flask import Flask
from flask_pymongo import PyMongo
from config import Config

# Initialize PyMongo extension (lazy initialization)
auth_mongo = PyMongo()

def create_app(config_class=Config):
    """Flask application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    app.config["MONGO_URI"] = app.config["AUTH_MONGO_URI"]  # Standardize naming
    auth_mongo.init_app(app)  # No need to pass uri separately

    # Register blueprints (example: auth blueprint)
    from app.routes.user_auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
