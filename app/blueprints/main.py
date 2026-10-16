from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from flask_login import current_user, login_required
from app.models import Crop, Livestock, PlantAssessment, AnimalTriageRecord
from app.services.i18n_service import SUPPORTED_LANGUAGES, t
from app.services.weather_service import get_weather_data
from app.blueprints.plant import checker as plant_checker_view
from app.blueprints.animal import triage as animal_triage_view
from app.blueprints.weather import index as weather_index_view
from app.blueprints.admin import index as admin_index_view

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home landing page for Smart Farmer AI."""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    weather = None
    default_district = 'Warangal, Telangana'
    if current_user.is_authenticated and current_user.district:
        default_district = f"{current_user.district}, {current_user.state or 'Telangana'}"
    weather = get_weather_data(default_district)
    return render_template('index.html', weather=weather)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Farmer personal dashboard with stats, recent activity, and advisories."""
    crops_count = Crop.query.filter_by(user_id=current_user.id).count()
    livestock_count = Livestock.query.filter_by(user_id=current_user.id).count()
    
    recent_assessments = PlantAssessment.query.filter_by(user_id=current_user.id)\
        .order_by(PlantAssessment.created_at.desc()).limit(5).all()
        
    recent_triages = AnimalTriageRecord.query.filter_by(user_id=current_user.id)\
        .order_by(AnimalTriageRecord.created_at.desc()).limit(5).all()
        
    my_crops = Crop.query.filter_by(user_id=current_user.id).order_by(Crop.created_at.desc()).limit(4).all()
    
    district_str = f"{current_user.district}, {current_user.state or 'Telangana'}"
    weather = get_weather_data(district_str)
    
    return render_template(
        'dashboard.html',
        crops_count=crops_count,
        livestock_count=livestock_count,
        recent_assessments=recent_assessments,
        recent_triages=recent_triages,
        my_crops=my_crops,
        weather=weather
    )


@main_bp.route('/set_language/<lang>')
def set_language(lang):
    """Switch application locale dynamically."""
    if lang in SUPPORTED_LANGUAGES:
        session['locale'] = lang
        if current_user.is_authenticated:
            try:
                from app import db
                current_user.preferred_language = lang
                db.session.commit()
            except Exception:
                pass
    referrer = request.referrer or url_for('main.index')
    return redirect(referrer)


@main_bp.route('/plant-checker', methods=['GET', 'POST'])
@login_required
def plant_checker_compat():
    return plant_checker_view()


@main_bp.route('/animal-checker', methods=['GET', 'POST'])
@login_required
def animal_checker_compat():
    return animal_triage_view()


@main_bp.route('/weather', methods=['GET'])
def weather_compat():
    return weather_index_view()


@main_bp.route('/admin', methods=['GET'])
def admin_compat():
    return admin_index_view()


@main_bp.route('/healthz')
def healthz():
    """Production health-check endpoint for Render / monitoring."""
    return jsonify({
        'status': 'healthy',
        'service': 'Smart Farmer AI',
        'database': 'connected',
        'supported_locales': list(SUPPORTED_LANGUAGES.keys())
    }), 200
