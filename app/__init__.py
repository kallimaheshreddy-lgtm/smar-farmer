import os
from datetime import datetime
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import config_by_name

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["500 per day", "100 per hour"],
    storage_uri="memory://"
)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
        
    app = Flask(__name__)
    cfg = config_by_name.get(config_name, config_by_name['development'])
    app.config.from_object(cfg)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access your farm and animal records.'
    login_manager.login_message_category = 'warning'

    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.plant import plant_bp
    from app.blueprints.animal import animal_bp
    from app.blueprints.weather import weather_bp
    from app.blueprints.farm import farm_bp
    from app.blueprints.knowledge import knowledge_bp
    from app.blueprints.livestock import livestock_bp
    from app.blueprints.vets import vets_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(plant_bp)
    app.register_blueprint(animal_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(farm_bp)
    app.register_blueprint(knowledge_bp)
    app.register_blueprint(livestock_bp)
    app.register_blueprint(vets_bp)
    app.register_blueprint(admin_bp)

    # Import localization helpers
    from app.services.i18n_service import t, get_current_locale, SUPPORTED_LANGUAGES

    @app.context_processor
    def inject_utilities():
        locale = get_current_locale()
        return {
            't': t,
            'current_locale': locale,
            'supported_languages': SUPPORTED_LANGUAGES,
            'current_year': datetime.now().year
        }

    # Custom Error Handlers
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html', error=e), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html', error=e), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html', error=e), 404

    @app.errorhandler(413)
    def file_too_large(e):
        return render_template('errors/413.html', error="Uploaded file exceeds maximum 8MB limit."), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html', error=e), 500

    # Ensure upload directory exists
    upload_dir = app.config.get('UPLOAD_FOLDER')
    if upload_dir:
        try:
            os.makedirs(upload_dir, exist_ok=True)
        except Exception:
            pass

    return app
