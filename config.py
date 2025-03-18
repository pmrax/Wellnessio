import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    AUTH_MONGO_URI = os.getenv("AUTH_MONGO_URI", "mongodb://localhost:27017/auth")


