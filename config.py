import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SECRET_KEY = os.getenv("SECRET_KEY")

    AUTH_MONGO_URI = os.getenv("AUTH_MONGO_URI")
    AI_MONGO_URI = os.getenv("AI_MONGO_URI")


