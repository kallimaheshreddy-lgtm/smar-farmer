import os
from datetime import datetime

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from app.models import AnimalAssessment, Farm, FarmExpense, KnowledgeBaseEntry, PlantAssessment, WeatherRecord, seed_example_knowledge
from app.services.animal_triage import triage_animal
from app.services.plant_ai import assess_plant

main_bp = Blueprint('main', __name__)


@main_bp.route('/set_language/<lang>')
def set_language(lang):
    if lang in current_app.config.get('LANGUAGES', ['en', 'hi', 'te']):
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))


@main_bp.route('/')
def index():
    weather_api_configured = bool(current_app.config.get('WEATHER_API_KEY'))
    return render_template('index.html', weather_api_configured=weather_api_configured)


@main_bp.route('/dashboard')
@login_required
def dashboard():
    farm_count = Farm.query.filter_by(user_id=current_user.id).count()
    latest_assessments = PlantAssessment.query.filter_by(user_id=current_user.id).order_by(PlantAssessment.created_at.desc()).limit(5).all()
    latest_animal = AnimalAssessment.query.filter_by(user_id=current_user.id).order_by(AnimalAssessment.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', farm_count=farm_count, latest_assessments=latest_assessments, latest_animal=latest_animal)


@main_bp.route('/plant-checker', methods=['GET', 'POST'])
@login_required
def plant_checker():
    result = None
    form_errors = []

    if request.method == 'POST':
        crop_type = (request.form.get('crop_type') or '').strip()
        crop_variety = (request.form.get('crop_variety') or '').strip()
        growth_stage = (request.form.get('growth_stage') or '').strip()
        symptoms = (request.form.get('symptoms') or '').strip()
        affected_area = (request.form.get('affected_area') or '').strip()

        if not crop_type or not symptoms:
            form_errors.append('Crop type and symptom details are required.')
        else:
            saved_paths = []
            uploaded = request.files.getlist('images')
            for upload in uploaded:
                if not upload or upload.filename == '':
                    continue
                filename = secure_filename(upload.filename)
                ext = os.path.splitext(filename)[1].lower()
                allowed_exts = {'.jpg', '.jpeg', '.png', '.webp'}
                if ext not in allowed_exts:
                    form_errors.append(f'Unsupported image type: {filename}. Use JPG, JPEG, PNG, or WEBP.')
                    continue
                if upload.content_length and upload.content_length > current_app.config['MAX_CONTENT_LENGTH']:
                    form_errors.append(f'Image too large: {filename}. Maximum size is 8 MB.')
                    continue
                if not hasattr(upload, 'stream'):
                    form_errors.append(f'Upload error for {filename}.')
                    continue
                upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                upload.save(upload_path)
                saved_paths.append(upload_path)

            if not form_errors:
                ai_result = assess_plant(saved_paths, crop_type=crop_type, variety=crop_variety, growth_stage=growth_stage, symptoms_text=symptoms)
                recommendation = (
                    'This is a safe manual assessment workflow. Inspect the affected plant parts, avoid spreading infection, and contact an agricultural extension officer if the problem is uncertain.'
                )
                diagnosis = 'Manual assessment completed.'
                model_status = 'manual'
                if ai_result:
                    diagnosis = ai_result.get('notes', 'AI model reported possible conditions.')
                    recommendation = ai_result.get('recommendation', recommendation)
                    model_status = 'ai'

                assessment = PlantAssessment(
                    user_id=current_user.id,
                    crop_type=crop_type,
                    growth_stage=growth_stage,
                    image_filename=saved_paths[0] if saved_paths else None,
                    symptoms_selected=', '.join([symptoms]),
                    symptoms_notes=symptoms,
                    detected_issue=diagnosis,
                    confidence=(ai_result.get('predictions', [{}])[0].get('confidence', 'N/A') if ai_result and ai_result.get('predictions') else 'N/A'),
                    assessment_mode='AI Model' if ai_result else 'Agronomic Screening',
                    reasons_supporting=diagnosis,
                    alternative_causes='No AI diagnosis available; manual inspection required.' if not ai_result else 'Possible disease or stress pattern requires agronomic review.',
                    recommended_steps=recommendation,
                    safety_precautions='Use gloves and wash hands after handling affected plants; avoid eating or smoking around diseased material.',
                    requires_expert_visit=not bool(ai_result),
                    created_at=datetime.utcnow(),
                )
                db.session.add(assessment)
                db.session.commit()
                result = {'diagnosis': diagnosis, 'recommendation': recommendation, 'model_status': model_status, 'ai_predictions': ai_result.get('predictions', []) if ai_result else []}
                flash('Assessment recorded successfully.', 'success')

    return render_template('plant_checker.html', result=result, form_errors=form_errors)


@main_bp.route('/animal-checker', methods=['GET', 'POST'])
@login_required
def animal_checker():
    result = None
    if request.method == 'POST':
        animal_type = (request.form.get('animal_type') or '').strip()
        symptoms = (request.form.get('symptoms') or '').strip()
        duration_days = request.form.get('duration_days')
        eating = (request.form.get('eating_behavior') or '').strip()
        drinking = (request.form.get('drinking_behavior') or '').strip()
        milk_change = (request.form.get('milk_change') or '').strip()
        pregnancy_status = (request.form.get('pregnancy_status') or '').strip()
        temperature_c = request.form.get('temperature_c')

        if not animal_type or not symptoms:
            flash('Animal type and symptoms are required.', 'danger')
        else:
            triage = triage_animal(symptoms, animal_type=animal_type)
            advice = (
                'Keep the animal calm, separate if needed, provide clean water, and contact a qualified veterinarian if symptoms are severe or worsening.'
            )
            if triage.get('category') == 'emergency':
                advice = 'Immediate veterinary attention is recommended. Urgent warning signs include breathing difficulty, collapse, severe bleeding, seizures, or inability to stand.'
            elif triage.get('category') == 'urgent':
                advice = 'Contact a veterinarian promptly and monitor the animal closely. Do not give human medicines without veterinary direction.'

            assessment = AnimalAssessment(
                user_id=current_user.id,
                animal_type=animal_type,
                age_months=request.form.get('age_months', type=int),
                weight_kg=request.form.get('weight_kg', type=float),
                symptoms=symptoms,
                duration_days=request.form.get('duration_days', type=int),
                eating_behavior=eating,
                drinking_behavior=drinking,
                milk_change=milk_change,
                pregnancy_status=pregnancy_status,
                temperature_c=request.form.get('temperature_c', type=float),
                triage_category=triage.get('category', 'routine'),
                advice=advice,
                created_at=datetime.utcnow(),
            )
            db.session.add(assessment)
            db.session.commit()
            result = {'category': triage.get('category', 'routine'), 'explanation': triage.get('explanation', 'Monitor the animal closely'), 'advice': advice}
            flash('Animal health assessment saved.', 'success')

    return render_template('animal_checker.html', result=result)


@main_bp.route('/farm-records', methods=['GET', 'POST'])
@login_required
def farm_records():
    if request.method == 'POST':
        name = (request.form.get('farm_name') or '').strip()
        if name:
            farm = Farm(
                user_id=current_user.id,
                name=name,
                total_area_acres=request.form.get('land_area', type=float) or 0.0,
                location=request.form.get('location') or '',
                soil_type='Black Cotton Soil',
                irrigation_source='Borewell'
            )
            db.session.add(farm)
            db.session.commit()
            flash('Farm record added.', 'success')

    farms = Farm.query.filter_by(user_id=current_user.id).all()
    expenses = FarmExpense.query.filter_by(user_id=current_user.id).order_by(FarmExpense.expense_date.desc()).limit(10).all()
    return render_template('farm_records.html', farms=farms, expenses=expenses)


@main_bp.route('/weather')
def weather():
    configured = bool(current_app.config.get('WEATHER_API_KEY'))
    sample = None
    if not configured:
        sample = {'alert': 'Weather API key is missing. Configure WEATHER_API_KEY to view live weather data.', 'temperature_c': '-', 'humidity': '-', 'rainfall_forecast_mm': '-'}
    return render_template('weather.html', configured=configured, sample=sample)


@main_bp.route('/knowledge-base')
def knowledge_base():
    entries = KnowledgeBaseEntry.query.order_by(KnowledgeBaseEntry.verification_date.desc().nullslast()).limit(20).all()
    return render_template('knowledge_base.html', entries=entries)


@main_bp.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    users = []
    from app.models import User
    users = User.query.order_by(User.created_at.desc()).all()
    entries = KnowledgeBaseEntry.query.order_by(KnowledgeBaseEntry.created_at.desc()).all()
    return render_template('admin.html', users=users, entries=entries)


@main_bp.route('/health')
def health():
    return {'status': 'ok', 'service': 'smart-farmer-ai'}

