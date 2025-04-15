from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from bson.objectid import ObjectId
import datetime
import re
import jwt
from flask import request, current_app
from app import auth_mongo

bcrypt = Bcrypt()  # Ensure bcrypt is initialized properly

class Customer(UserMixin):
    def __init__(self, customer_data):
        self.id = str(customer_data["_id"])
        self.username = customer_data.get("username")
        self.email = customer_data.get("email")
        self.mobile_no = customer_data.get("mobile_no")
        self.password_hash = customer_data.get("password_hash")
        self.profile_image = customer_data.get("profile_image", None)
        self.address = customer_data.get("address", {})
        self.created_at = customer_data.get("created_at", datetime.datetime.utcnow())
        self.last_login_ip = customer_data.get("last_login_ip")
        self.last_login_at = customer_data.get("last_login_at")

    @staticmethod
    def is_secure_password(password):
        """Checks password complexity."""
        return bool(re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

    @staticmethod
    def generate_jwt(customer_id):
        """Generates JWT token for authentication."""
        with current_app.app_context():
            secret_key = current_app.config.get("SECRET_KEY")
            if not secret_key:
                raise RuntimeError("SECRET_KEY is missing in the app configuration.")
            
            payload = {
                "customer_id": customer_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }
            return jwt.encode(payload, secret_key, algorithm="HS256")

    @staticmethod
    def register(username, email, mobile_no, password, confirm_password):
        """Registers a new customer."""
        if password != confirm_password:
            return {"error": "Passwords do not match."}
        if not Customer.is_secure_password(password):
            return {"error": "Password must be at least 8 characters long and include an uppercase letter, number, and special character."}

        existing_user = auth_mongo.db.customers.find_one({"$or": [{"email": email}, {"mobile_no": mobile_no}]})
        if existing_user:
            return {"error": "Email or mobile number already registered."}

        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        customer_data = {
            "username": username,
            "email": email,
            "mobile_no": mobile_no,
            "password_hash": password_hash,
            "profile_image": None,
            "address": {},
            "created_at": datetime.datetime.utcnow(),
            "failed_login_attempts": 0
        }

        inserted_id = auth_mongo.db.customers.insert_one(customer_data).inserted_id
        return {"success": "Registration successful!", "user_id": str(inserted_id)}

    @staticmethod
    def update_profile(customer_id, profile_image, address):
        """Updates customer profile, including address and profile image."""
        update_data = {"address": address}

        # Upload profile image to Cloudinary if provided
        if profile_image:
            image_url = Customer.upload_profile_image(profile_image)
            if image_url:
                update_data["profile_image"] = image_url

        # Update customer in database
        auth_mongo.db.customers.update_one({"_id": ObjectId(customer_id)}, {"$set": update_data})
        return {"success": "Profile updated successfully!"}

    @staticmethod
    def login(identifier, password):
        """Logs in a customer using email or mobile number."""
        user = auth_mongo.db.customers.find_one({"$or": [{"email": identifier}, {"mobile_no": identifier}]})
        if not user:
            return {"error": "Invalid credentials."}

        if user.get("failed_login_attempts", 0) >= 5:
            return {"error": "Too many failed attempts. Try again later."}

        if bcrypt.check_password_hash(user["password_hash"], password):
            ip_address = request.remote_addr
            auth_mongo.db.customers.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login_ip": ip_address, "last_login_at": datetime.datetime.utcnow(), "failed_login_attempts": 0}}
            )
            token = Customer.generate_jwt(str(user["_id"]))
            return {"customer": Customer(user), "token": token}

        auth_mongo.db.customers.update_one(
            {"_id": user["_id"]},
            {"$inc": {"failed_login_attempts": 1}}
        )
        return {"error": "Invalid credentials."}

    @staticmethod
    def update_password(customer_id, new_password):
        """Updates password."""
        if not Customer.is_secure_password(new_password):
            return {"error": "Password does not meet security requirements."}

        password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
        auth_mongo.db.customers.update_one(
            {"_id": ObjectId(customer_id)},
            {"$set": {"password_hash": password_hash}}
        )
        return {"success": "Password updated successfully!"}

    @staticmethod
    def get_customer_by_id(customer_id):
        """Fetches customer details by ID."""
        user = auth_mongo.db.customers.find_one({"_id": ObjectId(customer_id)})
        return Customer(user) if user else None
