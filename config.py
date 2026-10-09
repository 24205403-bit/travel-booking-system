import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'travel_booking_super_secret_key_2026_x99')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/travel_booking')
    DB_NAME = os.getenv('DB_NAME', 'travel_booking')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit

    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'larancebjothi@gmail.com')

    # Required by flask-dance to allow HTTP in development
    OAUTHLIB_INSECURE_TRANSPORT = '1'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
