import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from app import db
from app.models import AnimalTriageRecord, Livestock
from app.services.animal_service import evaluate_animal_triage
from app.services.plant_service import validate_image_file

animal_bp = Blueprint('animal', __name__, url_prefix='/animal')


@animal_bp.route('/triage', methods=['GET', 'POST'])
def triage():
    """Conservative livestock veterinary triage workflow."""
    user_livestock = []
    if current_user.is_authenticated:
        user_livestock = Livestock.query.filter_by(user_id=current_user.id).all()
        
    if request.method == 'POST':
        file = request.files.get('animal_image')
        raw_species = request.form.get('species', '').strip()
        species = raw_species if raw_species else ('Livestock (Photo Diagnosed)' if file and file.filename else 'Cow')
        livestock_id = request.form.get('livestock_id')
        age_approx = request.form.get('age_approx', '').strip()
        symptoms_selected = request.form.getlist('symptoms')
        symptoms_notes = request.form.get('symptoms_notes', '').strip()
        appetite = request.form.get('appetite', 'normal')
        behavior = request.form.get('behavior', 'alert')
        temperature_status = request.form.get('temperature_status', 'normal')
        breathing_status = request.form.get('breathing_status', 'normal')
        standing_status = request.form.get('standing_status', 'normal')
        milk_yield_drop = request.form.get('milk_yield_drop', 'none')

        # Handle optional animal symptom photo
        image_filename = None
        file = request.files.get('animal_image')
        if file and file.filename:
            is_valid, err_msg, sanitized_name = validate_image_file(file)
            if is_valid:
                ext = sanitized_name.rsplit('.', 1)[1].lower()
                unique_name = f"animal_{uuid.uuid4().hex[:12]}.{ext}"
                upload_dir = current_app.config.get('UPLOAD_FOLDER')
                os.makedirs(upload_dir, exist_ok=True)
                save_path = os.path.join(upload_dir, unique_name)
                file.save(save_path)
                image_filename = unique_name
            else:
                flash(err_msg, 'warning')
        
        triage_eval = evaluate_animal_triage(
            species=species,
            age_approx=age_approx,
            symptoms_selected=", ".join(symptoms_selected),
            symptoms_notes=symptoms_notes,
            appetite=appetite,
            behavior=behavior,
            temperature_status=temperature_status,
            breathing_status=breathing_status,
            standing_status=standing_status,
            milk_yield_drop=milk_yield_drop,
            image_filename=image_filename
        )
        
        record = AnimalTriageRecord(
            user_id=current_user.id if current_user.is_authenticated else None,
            livestock_id=int(livestock_id) if livestock_id and livestock_id.isdigit() else None,
            species=species,
            image_filename=image_filename,
            age_approx=age_approx,
            symptoms_selected=", ".join(symptoms_selected),
            symptoms_notes=symptoms_notes,
            appetite=appetite,
            behavior=behavior,
            temperature_status=temperature_status,
            breathing_status=breathing_status,
            standing_status=standing_status,
            urgency_level=triage_eval['urgency_level'],
            immediate_guidance=triage_eval['interim_guidance'],
            what_not_to_do=triage_eval['what_not_to_do'],
            requires_immediate_vet=triage_eval['requires_immediate_vet']
        )
        db.session.add(record)
        db.session.commit()
        
        return render_template(
            'animal/result.html',
            record=record,
            eval_data=triage_eval
        )
        
    return render_template('animal/triage.html', user_livestock=user_livestock)


@animal_bp.route('/history')
@login_required
def history():
    """Farmer's past veterinary triage assessments."""
    records = AnimalTriageRecord.query.filter_by(user_id=current_user.id)\
        .order_by(AnimalTriageRecord.created_at.desc()).all()
    return render_template('animal/history.html', records=records)


@animal_bp.route('/view/<int:record_id>')
def view_record(record_id):
    """View details of a past triage evaluation."""
    record = AnimalTriageRecord.query.get_or_404(record_id)
    if record.user_id and current_user.is_authenticated and record.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access to private animal record.', 'danger')
        return redirect(url_for('animal.history'))
    return render_template('animal/result.html', record=record, eval_data=record)


@animal_bp.route('/quick-solve', methods=['POST'])
def quick_solve():
    """
    1-Click Instant Animal Health Triage via Photo:
    Farmer snaps or uploads a photo of the affected livestock (cow, buffalo, goat, sheep, poultry),
    and immediately receives urgent triage rating, interim safe first aid, what NOT to do, and 1962 helpline.
    """
    species = request.form.get('species', 'Livestock / Domestic Animal').strip()
    file = request.files.get('animal_image')
    if not file or not file.filename:
        flash('Please take a photo or select an image of the animal.', 'warning')
        return redirect(url_for('animal.triage'))

    is_valid, err_msg, sanitized_name = validate_image_file(file)
    if not is_valid:
        flash(err_msg, 'danger')
        return redirect(url_for('animal.triage'))

    ext = sanitized_name.rsplit('.', 1)[1].lower()
    unique_name = f"animal_{uuid.uuid4().hex[:12]}.{ext}"
    upload_dir = current_app.config.get('UPLOAD_FOLDER')
    os.makedirs(upload_dir, exist_ok=True)
    save_path = os.path.join(upload_dir, unique_name)
    file.save(save_path)

    # Perform automated triage evaluation with visual inspection
    triage_eval = evaluate_animal_triage(
        species=species,
        symptoms_selected='Photo Visual Health Screening',
        symptoms_notes='1-Click Instant Photo Animal Assessment',
        image_filename=unique_name
    )

    record = AnimalTriageRecord(
        user_id=current_user.id if current_user.is_authenticated else None,
        species=species,
        image_filename=unique_name,
        age_approx='Field photo',
        symptoms_selected='Photo Visual Health Screening',
        symptoms_notes='Instant camera capture in field',
        appetite='normal',
        behavior='alert',
        temperature_status='normal',
        breathing_status='normal',
        standing_status='normal',
        urgency_level=triage_eval['urgency_level'],
        immediate_guidance=triage_eval['interim_guidance'],
        what_not_to_do=triage_eval['what_not_to_do'],
        requires_immediate_vet=triage_eval['requires_immediate_vet']
    )
    db.session.add(record)
    db.session.commit()

    flash('Animal photo assessed successfully! Follow the interim nursing guidance and call 1962 if urgent.', 'info')
    return render_template('animal/result.html', record=record, eval_data=triage_eval)

