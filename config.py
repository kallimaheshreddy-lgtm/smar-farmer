import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def normalize_database_url(db_url):
    if db_url.startswith('postgres://'):
        return db_url.replace('postgres://', 'postgresql+psycopg://', 1)
    if db_url.startswith('postgresql://'):
        return db_url.replace('postgresql://', 'postgresql+psycopg://', 1)
    return db_url


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'local-development-only-change-me')
    
    # Use psycopg 3 for PostgreSQL URLs on both Windows and production hosts.
    SQLALCHEMY_DATABASE_URI = normalize_database_url(
        os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "faemer.db"}')
    )
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
    SECRET_KEY = None
    SESSION_COOKIE_SECURE = True


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
