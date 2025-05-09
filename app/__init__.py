import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from dotenv import load_dotenv
from config import Config

# Load environment variables
load_dotenv()

# Initialize PyMongo instances
auth_mongo = PyMongo()
ai_mongo = PyMongo()

# Initialize Flask-Login
login_manager = LoginManager()

def create_app(config_class=Config):
    """Flask application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Debugging: Check if SECRET_KEY is loaded correctly
    print("Loaded SECRET_KEY:", repr(app.config["SECRET_KEY"]))

    # Ensure SECRET_KEY is set properly
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY is not set! Please set it in the environment or config file.")

    # Initialize MongoDB connections with distinct URIs
    auth_mongo.init_app(app, uri=app.config["AUTH_MONGO_URI"])
    ai_mongo.init_app(app, uri=app.config["AI_MONGO_URI"])

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"  # Redirect to login page if unauthorized

    # Define user loader function for Flask-Login
    from app.authentication.user_auth_model import Customer

    @login_manager.user_loader
    def load_user(user_id):
        """Loads user from the database using Flask-Login."""
        return Customer.get_customer_by_id(user_id)

    # Register blueprints
    from app.authentication.user_auth_routes import auth_bp
    from app.ai.medicine_routes import ai_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(ai_bp)

    return app



