from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from app.models import Livestock, VetVisit

livestock_bp = Blueprint('livestock', __name__, url_prefix='/livestock')


@livestock_bp.route('/')
@login_required
def index():
    """Farmer's livestock profiles and veterinary visit logs."""
    animals = Livestock.query.filter_by(user_id=current_user.id).order_by(Livestock.created_at.desc()).all()
    visits = VetVisit.query.filter_by(user_id=current_user.id).order_by(VetVisit.visit_date.desc()).limit(10).all()
    
    species_counts = {}
    for a in animals:
        species_counts[a.species] = species_counts.get(a.species, 0) + 1
        
    return render_template(
        'livestock/index.html',
        animals=animals,
        visits=visits,
        species_counts=species_counts
    )


@livestock_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_animal():
    if request.method == 'POST':
        tag_id = request.form.get('tag_id', '').strip()
        name = request.form.get('name', '').strip()
        species = request.form.get('species', 'Cow').strip()
        breed = request.form.get('breed', '').strip()
        age_months = int(request.form.get('age_months', 12) or 12)
        gender = request.form.get('gender', 'Female')
        health_status = request.form.get('health_status', 'Healthy')
        reproductive_status = request.form.get('reproductive_status', 'Lactating')
        notes = request.form.get('notes', '').strip()
        
        if not tag_id:
            flash('Tag ID / Identifier is required for livestock tracking.', 'warning')
            return render_template('livestock/animal_form.html', action='Add', animal=None)
            
        animal = Livestock(
            user_id=current_user.id,
            tag_id=tag_id,
            name=name,
            species=species,
            breed=breed,
            age_months=age_months,
            gender=gender,
            health_status=health_status,
            reproductive_status=reproductive_status,
            notes=notes
        )
        db.session.add(animal)
        db.session.commit()
        flash(f'Livestock profile "{tag_id}" registered successfully.', 'success')
        return redirect(url_for('livestock.index'))
        
    return render_template('livestock/animal_form.html', action='Add', animal=None)


@livestock_bp.route('/edit/<int:animal_id>', methods=['GET', 'POST'])
@login_required
def edit_animal(animal_id):
    animal = Livestock.query.filter_by(id=animal_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        animal.tag_id = request.form.get('tag_id', animal.tag_id).strip()
        animal.name = request.form.get('name', animal.name).strip()
        animal.species = request.form.get('species', animal.species).strip()
        animal.breed = request.form.get('breed', animal.breed).strip()
        animal.age_months = int(request.form.get('age_months', animal.age_months) or animal.age_months)
        animal.gender = request.form.get('gender', animal.gender)
        animal.health_status = request.form.get('health_status', animal.health_status)
        animal.reproductive_status = request.form.get('reproductive_status', animal.reproductive_status)
        animal.notes = request.form.get('notes', animal.notes).strip()
        
        db.session.commit()
        flash(f'Animal profile "{animal.tag_id}" updated successfully.', 'success')
        return redirect(url_for('livestock.index'))
        
    return render_template('livestock/animal_form.html', action='Edit', animal=animal)


@livestock_bp.route('/delete/<int:animal_id>', methods=['POST'])
@login_required
def delete_animal(animal_id):
    animal = Livestock.query.filter_by(id=animal_id, user_id=current_user.id).first_or_404()
    db.session.delete(animal)
    db.session.commit()
    flash(f'Animal profile "{animal.tag_id}" removed from records.', 'info')
    return redirect(url_for('livestock.index'))


@livestock_bp.route('/vet_visit/add', methods=['GET', 'POST'])
@login_required
def add_vet_visit():
    animals = Livestock.query.filter_by(user_id=current_user.id).all()
    
    if request.method == 'POST':
        livestock_id = request.form.get('livestock_id')
        vet_name = request.form.get('vet_name', '').strip()
        clinic_name = request.form.get('clinic_name', '').strip()
        phone = request.form.get('phone', '').strip()
        reason = request.form.get('reason', '').strip()
        diagnosis_notes = request.form.get('diagnosis_notes', '').strip()
        advice_given = request.form.get('advice_given', '').strip()
        cost = float(request.form.get('cost', 0.0) or 0.0)
        visit_date_str = request.form.get('visit_date')
        follow_up_str = request.form.get('follow_up_date')
        
        if not vet_name or not reason:
            flash('Veterinarian name and reason for visit are required.', 'warning')
            return render_template('livestock/vet_visit_form.html', animals=animals)
            
        visit_date = datetime.utcnow().date()
        if visit_date_str:
            try:
                visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
                
        follow_up = None
        if follow_up_str:
            try:
                follow_up = datetime.strptime(follow_up_str, '%Y-%m-%d').date()
            except ValueError:
                pass
                
        visit = VetVisit(
            user_id=current_user.id,
            livestock_id=int(livestock_id) if livestock_id and livestock_id.isdigit() else None,
            vet_name=vet_name,
            clinic_name=clinic_name,
            phone=phone,
            reason=reason,
            diagnosis_notes=diagnosis_notes,
            advice_given=advice_given,
            cost=cost,
            visit_date=visit_date,
            follow_up_date=follow_up
        )
        db.session.add(visit)
        db.session.commit()
        flash('Veterinary consultation logged successfully.', 'success')
        return redirect(url_for('livestock.index'))
        
    return render_template('livestock/vet_visit_form.html', animals=animals)
