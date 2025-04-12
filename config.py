import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "1#23@drc324f2#$%@#$FFC32@$3423")  # Ensure it never becomes None
    
    # MongoDB database connection in local system.
    AUTH_MONGO_URI = os.getenv("AUTH_MONGO_URI", "mongodb://localhost:27017/auth")



