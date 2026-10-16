import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart-farmer-ai-prod-key-7788442299')
    
    # Handle Render / Heroku postgresql:// vs postgres:// URL format
    db_url = os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "faemer.db"}')
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', str(BASE_DIR / 'app' / 'static' / 'uploads'))
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB max upload limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
    
    # Localization
    SUPPORTED_LANGUAGES = ['en', 'te', 'hi']
    LANGUAGES = SUPPORTED_LANGUAGES
    DEFAULT_LANGUAGE = 'en'
    
    # AI and Weather Integrations
    MODEL_API_URL = os.environ.get('MODEL_API_URL')
    MODEL_API_KEY = os.environ.get('MODEL_API_KEY')
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
    
    # Rate Limiting & Security
    RATELIMIT_DEFAULT = "200 per day; 50 per hour"
    RATELIMIT_STORAGE_URI = "memory://"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
