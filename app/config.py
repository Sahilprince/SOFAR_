import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Ensure MONGO_URI is correctly set from environment variable
    MONGO_URI = os.getenv('MONGODB_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')