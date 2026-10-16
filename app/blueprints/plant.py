import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from app import db
from app.models import PlantAssessment, Crop
from app.services.plant_service import (
    validate_image_file,
    RemoteModelAdapter,
    perform_agronomic_assessment
)

plant_bp = Blueprint('plant', __name__, url_prefix='/plant')


@plant_bp.route('/checker', methods=['GET', 'POST'])
def checker():
    """Plant Disease & Health Checker with dual AI/Agronomic verification pipeline."""
    user_crops = []
    if current_user.is_authenticated:
        user_crops = Crop.query.filter_by(user_id=current_user.id).all()
        
    if request.method == 'POST':
        crop_type = request.form.get('crop_type', '').strip()
        growth_stage = request.form.get('growth_stage', '').strip()
        crop_id = request.form.get('crop_id')
        affected_parts = request.form.get('affected_parts', '').strip()
        symptoms_selected = request.form.getlist('symptoms')
        symptoms_notes = request.form.get('symptoms_notes', '').strip()
        symptoms_combined = ", ".join(symptoms_selected)
        if symptoms_notes:
            symptoms_combined += f" ({symptoms_notes})"
            
        if not crop_type:
            flash('Please select or specify a crop type.', 'warning')
            return render_template('plant/checker.html', user_crops=user_crops)
            
        # File upload handling
        image_filename = None
        file = request.files.get('plant_image')
        if file and file.filename:
            is_valid, err_msg, sanitized_name = validate_image_file(file)
            if not is_valid:
                flash(err_msg, 'danger')
                return render_template('plant/checker.html', user_crops=user_crops)
                
            # Save safely with UUID prefix to prevent collisions
            ext = sanitized_name.rsplit('.', 1)[1].lower()
            unique_name = f"plant_{uuid.uuid4().hex[:12]}.{ext}"
            upload_dir = current_app.config.get('UPLOAD_FOLDER')
            os.makedirs(upload_dir, exist_ok=True)
            save_path = os.path.join(upload_dir, unique_name)
            file.save(save_path)
            image_filename = unique_name
            
        # AI Model Integration Check
        model_adapter = RemoteModelAdapter()
        assessment_result = None
        
        if model_adapter.is_configured() and image_filename:
            upload_dir = current_app.config.get('UPLOAD_FOLDER')
            img_path = os.path.join(upload_dir, image_filename)
            ai_resp, err = model_adapter.predict(img_path, crop_type=crop_type, symptoms=symptoms_combined)
            if ai_resp and 'predictions' in ai_resp:
                top_pred = ai_resp['predictions'][0]
                assessment_result = {
                    'detected_issue': top_pred.get('label', 'Condition Detected'),
                    'confidence': f"{round(float(top_pred.get('confidence', 0.8)) * 100, 1)}% (Deep Learning Model)",
                    'assessment_mode': 'Automated Deep Learning Classifier',
                    'reasons_supporting': ai_resp.get('notes', 'Visual features matched trained model patterns.'),
                    'alternative_causes': 'Secondary infections or physiological stress.',
                    'recommended_steps': 'Refer to local Krishi Vigyan Kendra for confirmation.',
                    'safety_precautions': 'Wear protective equipment during any agricultural operations.',
                    'source_institution': 'Integrated AI Model Endpoint',
                    'review_date': 'Live Model Inference',
                    'requires_expert_visit': True,
                    'model_configured': True
                }
                
        # If AI model is not configured or no prediction returned:
        if not assessment_result:
            assessment_result = perform_agronomic_assessment(
                crop_type=crop_type,
                symptoms_text=symptoms_combined,
                growth_stage=growth_stage,
                affected_parts=affected_parts,
                image_filename=image_filename
            )
            
        # Save record in database
        assessment = PlantAssessment(
            user_id=current_user.id if current_user.is_authenticated else None,
            crop_id=int(crop_id) if crop_id and crop_id.isdigit() else None,
            crop_type=crop_type,
            growth_stage=growth_stage,
            image_filename=image_filename,
            symptoms_selected=", ".join(symptoms_selected),
            symptoms_notes=symptoms_notes,
            detected_issue=assessment_result['detected_issue'],
            confidence=assessment_result['confidence'],
            assessment_mode=assessment_result['assessment_mode'],
            reasons_supporting=assessment_result['reasons_supporting'],
            alternative_causes=assessment_result['alternative_causes'],
            recommended_steps=assessment_result['recommended_steps'],
            safety_precautions=assessment_result['safety_precautions'],
            source_institution=assessment_result['source_institution'],
            review_date=assessment_result['review_date'],
            requires_expert_visit=assessment_result['requires_expert_visit']
        )
        db.session.add(assessment)
        db.session.commit()
        
        return render_template(
            'plant/result.html',
            assessment=assessment,
            result=assessment_result
        )
        
    return render_template('plant/checker.html', user_crops=user_crops)


@plant_bp.route('/history')
@login_required
def history():
    """Farmer's past plant assessments."""
    records = PlantAssessment.query.filter_by(user_id=current_user.id)\
        .order_by(PlantAssessment.created_at.desc()).all()
    return render_template('plant/history.html', records=records)


@plant_bp.route('/view/<int:assessment_id>')
def view_assessment(assessment_id):
    """View details of a past assessment."""
    assessment = PlantAssessment.query.get_or_404(assessment_id)
    if assessment.user_id and current_user.is_authenticated and assessment.user_id != current_user.id and not current_user.is_admin:
        flash('Unauthorized access to private farmer record.', 'danger')
        return redirect(url_for('plant.history'))
    return render_template('plant/result.html', assessment=assessment, result=assessment)
