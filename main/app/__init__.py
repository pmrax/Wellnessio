from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from dotenv import load_dotenv
from config import Config

load_dotenv()

auth_mongo = PyMongo()
ai_mongo = PyMongo()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    print("Loaded SECRET_KEY:", repr(app.config["SECRET_KEY"]))

    if not app.config["SECRET_KEY"]:
        raise RuntimeError("SECRET_KEY is not set! Please set it in the environment or config file.")

    auth_mongo.init_app(app, uri=app.config["AUTH_MONGO_URI"])
    ai_mongo.init_app(app, uri=app.config["AI_MONGO_URI"])

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.authentication.user_auth_model import Customer

    @login_manager.user_loader
    def load_user(user_id):
        return Customer.get_customer_by_id(user_id)

    from app.authentication.user_auth_routes import auth_bp
    from app.ai.medicine_routes import ai_bp
    from app.public.public_routes import public_bp
    from app.authenticated.profile_routes import profile_bp
    from app.market.market_routes import market_bp
    from app.market.customer.routes.profile_routes import market_profile_bp
    from app.market.seller.routes.seller_auth_routes import seller_auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(market_profile_bp, url_prefix="/market")
    app.register_blueprint(seller_auth_bp, url_prefix="/market")

    return app
