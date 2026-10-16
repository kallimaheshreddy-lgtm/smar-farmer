from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import Crop, FarmActivity

farm_bp = Blueprint('farm', __name__, url_prefix='/farm')


@farm_bp.route('/')
@login_required
def index():
    """My Farm overview: crops, field records, and activity timeline."""
    crops = Crop.query.filter_by(user_id=current_user.id).order_by(Crop.created_at.desc()).all()
    activities = FarmActivity.query.filter_by(user_id=current_user.id)\
        .order_by(FarmActivity.activity_date.desc()).limit(15).all()
    total_area = sum(c.area_acres or 0 for c in crops)
    total_expenses = sum(a.cost or 0 for a in activities)
    
    return render_template(
        'farm/index.html',
        crops=crops,
        activities=activities,
        total_area=round(total_area, 2),
        total_expenses=round(total_expenses, 2)
    )


@farm_bp.route('/crop/add', methods=['GET', 'POST'])
@login_required
def add_crop():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        variety = request.form.get('variety', '').strip()
        field_name = request.form.get('field_name', 'Main Plot').strip()
        area_acres = float(request.form.get('area_acres', 1.0) or 1.0)
        planting_date_str = request.form.get('planting_date')
        expected_harvest_str = request.form.get('expected_harvest_date')
        status = request.form.get('status', 'Growing')
        
        if not name:
            flash('Crop name is required.', 'warning')
            return render_template('farm/crop_form.html', action='Add', crop=None)
            
        planting_date = None
        if planting_date_str:
            try:
                planting_date = datetime.strptime(planting_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
                
        expected_harvest = None
        if expected_harvest_str:
            try:
                expected_harvest = datetime.strptime(expected_harvest_str, '%Y-%m-%d').date()
            except ValueError:
                pass
                
        crop = Crop(
            user_id=current_user.id,
            name=name,
            variety=variety,
            field_name=field_name,
            area_acres=area_acres,
            planting_date=planting_date,
            expected_harvest_date=expected_harvest,
            status=status
        )
        db.session.add(crop)
        db.session.commit()
        flash(f'Crop "{name}" added successfully to your farm records.', 'success')
        return redirect(url_for('farm.index'))
        
    return render_template('farm/crop_form.html', action='Add', crop=None)


@farm_bp.route('/crop/edit/<int:crop_id>', methods=['GET', 'POST'])
@login_required
def edit_crop(crop_id):
    crop = Crop.query.filter_by(id=crop_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        crop.name = request.form.get('name', crop.name).strip()
        crop.variety = request.form.get('variety', crop.variety).strip()
        crop.field_name = request.form.get('field_name', crop.field_name).strip()
        crop.area_acres = float(request.form.get('area_acres', crop.area_acres) or crop.area_acres)
        crop.status = request.form.get('status', crop.status)
        
        planting_date_str = request.form.get('planting_date')
        if planting_date_str:
            try:
                crop.planting_date = datetime.strptime(planting_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
                
        expected_harvest_str = request.form.get('expected_harvest_date')
        if expected_harvest_str:
            try:
                crop.expected_harvest_date = datetime.strptime(expected_harvest_str, '%Y-%m-%d').date()
            except ValueError:
                pass
                
        db.session.commit()
        flash(f'Crop "{crop.name}" updated successfully.', 'success')
        return redirect(url_for('farm.index'))
        
    return render_template('farm/crop_form.html', action='Edit', crop=crop)


@farm_bp.route('/crop/delete/<int:crop_id>', methods=['POST'])
@login_required
def delete_crop(crop_id):
    crop = Crop.query.filter_by(id=crop_id, user_id=current_user.id).first_or_404()
    db.session.delete(crop)
    db.session.commit()
    flash(f'Crop "{crop.name}" deleted from your farm.', 'info')
    return redirect(url_for('farm.index'))


@farm_bp.route('/activity/add', methods=['GET', 'POST'])
@login_required
def add_activity():
    crops = Crop.query.filter_by(user_id=current_user.id).all()
    
    if request.method == 'POST':
        crop_id = request.form.get('crop_id')
        activity_type = request.form.get('activity_type', 'Irrigation')
        description = request.form.get('description', '').strip()
        quantity = request.form.get('quantity', '').strip()
        cost = float(request.form.get('cost', 0.0) or 0.0)
        activity_date_str = request.form.get('activity_date')
        
        if not description:
            flash('Activity description is required.', 'warning')
            return render_template('farm/activity_form.html', crops=crops)
            
        act_date = datetime.utcnow().date()
        if activity_date_str:
            try:
                act_date = datetime.strptime(activity_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
                
        activity = FarmActivity(
            user_id=current_user.id,
            crop_id=int(crop_id) if crop_id and crop_id.isdigit() else None,
            activity_type=activity_type,
            description=description,
            quantity=quantity,
            cost=cost,
            activity_date=act_date
        )
        db.session.add(activity)
        db.session.commit()
        flash('Farm activity logged successfully.', 'success')
        return redirect(url_for('farm.index'))
        
    return render_template('farm/activity_form.html', crops=crops)
