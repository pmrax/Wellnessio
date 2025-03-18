import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")  # Ensure it never becomes None
    AUTH_MONGO_URI = os.getenv("AUTH_MONGO_URI", "mongodb://localhost:27017/auth")
