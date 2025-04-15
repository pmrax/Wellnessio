import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "hello@wellnessio")  # Ensure it never becomes None
    
    # MongoDB database connection in local system.
    AUTH_MONGO_URI = os.getenv("AUTH_MONGO_URI", "mongodb://localhost:27017/auth")
    AI_MONGO_URI = os.getenv("AI_MONGO_URI", "mongodb://localhost:27017/wellnessio_ai")



