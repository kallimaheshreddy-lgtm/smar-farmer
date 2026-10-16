from datetime import datetime
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from app import db
from app.models import (
    User, Crop, Livestock, PlantAssessment,
    AnimalTriageRecord, KnowledgeArticle, VetContact
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Administrator privileges required to access this portal.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard with high-level analytics and management links."""
    total_users = User.query.count()
    total_crops = Crop.query.count()
    total_livestock = Livestock.query.count()
    total_assessments = PlantAssessment.query.count()
    total_triages = AnimalTriageRecord.query.count()
    total_articles = KnowledgeArticle.query.count()
    total_vets = VetContact.query.count()
    
    recent_assessments = PlantAssessment.query.order_by(PlantAssessment.created_at.desc()).limit(6).all()
    recent_triages = AnimalTriageRecord.query.order_by(AnimalTriageRecord.created_at.desc()).limit(6).all()
    
    return render_template(
        'admin/index.html',
        total_users=total_users,
        total_crops=total_crops,
        total_livestock=total_livestock,
        total_assessments=total_assessments,
        total_triages=total_triages,
        total_articles=total_articles,
        total_vets=total_vets,
        recent_assessments=recent_assessments,
        recent_triages=recent_triages
    )


@admin_bp.route('/knowledge')
@login_required
@admin_required
def knowledge_list():
    """Manage knowledge base entries."""
    articles = KnowledgeArticle.query.order_by(KnowledgeArticle.category, KnowledgeArticle.title).all()
    return render_template('admin/knowledge_list.html', articles=articles)


@admin_bp.route('/knowledge/add', methods=['GET', 'POST'])
@login_required
@admin_required
def knowledge_add():
    if request.method == 'POST':
        category = request.form.get('category')
        title = request.form.get('title', '').strip()
        crop_or_animal = request.form.get('crop_or_animal', '').strip()
        symptoms_description = request.form.get('symptoms_description', '').strip()
        management_practices = request.form.get('management_practices', '').strip()
        organic_options = request.form.get('organic_options', '').strip()
        safety_precautions = request.form.get('safety_precautions', '').strip()
        source_institution = request.form.get('source_institution', '').strip()
        last_reviewed_date = request.form.get('last_reviewed_date', '').strip() or datetime.utcnow().strftime('%B %Y')
        
        if not title or not management_practices or not source_institution:
            flash('Title, Management Practices, and Source Institution are required.', 'warning')
            return render_template('admin/knowledge_form.html', action='Add', article=None)
            
        article = KnowledgeArticle(
            category=category,
            title=title,
            crop_or_animal=crop_or_animal,
            symptoms_description=symptoms_description,
            management_practices=management_practices,
            organic_options=organic_options,
            safety_precautions=safety_precautions,
            source_institution=source_institution,
            last_reviewed_date=last_reviewed_date,
            is_active=True
        )
        db.session.add(article)
        db.session.commit()
        flash(f'Knowledge base entry "{title}" added successfully.', 'success')
        return redirect(url_for('admin.knowledge_list'))
        
    return render_template('admin/knowledge_form.html', action='Add', article=None)


@admin_bp.route('/knowledge/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def knowledge_edit(article_id):
    article = KnowledgeArticle.query.get_or_404(article_id)
    
    if request.method == 'POST':
        article.category = request.form.get('category')
        article.title = request.form.get('title', article.title).strip()
        article.crop_or_animal = request.form.get('crop_or_animal', article.crop_or_animal).strip()
        article.symptoms_description = request.form.get('symptoms_description', article.symptoms_description).strip()
        article.management_practices = request.form.get('management_practices', article.management_practices).strip()
        article.organic_options = request.form.get('organic_options', article.organic_options).strip()
        article.safety_precautions = request.form.get('safety_precautions', article.safety_precautions).strip()
        article.source_institution = request.form.get('source_institution', article.source_institution).strip()
        article.last_reviewed_date = request.form.get('last_reviewed_date', article.last_reviewed_date).strip()
        article.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        flash(f'Article "{article.title}" updated successfully.', 'success')
        return redirect(url_for('admin.knowledge_list'))
        
    return render_template('admin/knowledge_form.html', action='Edit', article=article)


@admin_bp.route('/knowledge/toggle/<int:article_id>', methods=['POST'])
@login_required
@admin_required
def knowledge_toggle(article_id):
    """Deactivate or activate an article to prevent outdated advice."""
    article = KnowledgeArticle.query.get_or_404(article_id)
    article.is_active = not article.is_active
    db.session.commit()
    status_str = "activated" if article.is_active else "deactivated"
    flash(f'Article "{article.title}" {status_str}.', 'info')
    return redirect(url_for('admin.knowledge_list'))


@admin_bp.route('/vets')
@login_required
@admin_required
def vets_list():
    """Manage veterinary contacts directory."""
    contacts = VetContact.query.order_by(VetContact.state, VetContact.district, VetContact.name).all()
    return render_template('admin/vets_list.html', contacts=contacts)


@admin_bp.route('/vets/add', methods=['GET', 'POST'])
@login_required
@admin_required
def vets_add():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        contact_type = request.form.get('contact_type', 'Govt Veterinary Dispensary')
        state = request.form.get('state', '').strip()
        district = request.form.get('district', '').strip()
        address = request.form.get('address', '').strip()
        phone = request.form.get('phone', '').strip()
        emergency_phone = request.form.get('emergency_phone', '1962').strip()
        email = request.form.get('email', '').strip()
        
        if not name or not state or not district or not phone:
            flash('Name, State, District, and Phone are required.', 'warning')
            return render_template('admin/vet_form.html', action='Add', contact=None)
            
        contact = VetContact(
            name=name,
            contact_type=contact_type,
            state=state,
            district=district,
            address=address,
            phone=phone,
            emergency_phone=emergency_phone,
            email=email,
            is_active=True
        )
        db.session.add(contact)
        db.session.commit()
        flash(f'Veterinary directory entry "{name}" added successfully.', 'success')
        return redirect(url_for('admin.vets_list'))
        
    return render_template('admin/vet_form.html', action='Add', contact=None)


@admin_bp.route('/vets/edit/<int:contact_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def vets_edit(contact_id):
    contact = VetContact.query.get_or_404(contact_id)
    
    if request.method == 'POST':
        contact.name = request.form.get('name', contact.name).strip()
        contact.contact_type = request.form.get('contact_type', contact.contact_type)
        contact.state = request.form.get('state', contact.state).strip()
        contact.district = request.form.get('district', contact.district).strip()
        contact.address = request.form.get('address', contact.address).strip()
        contact.phone = request.form.get('phone', contact.phone).strip()
        contact.emergency_phone = request.form.get('emergency_phone', contact.emergency_phone).strip()
        contact.email = request.form.get('email', contact.email).strip()
        contact.is_active = bool(request.form.get('is_active'))
        
        db.session.commit()
        flash(f'Contact "{contact.name}" updated successfully.', 'success')
        return redirect(url_for('admin.vets_list'))
        
    return render_template('admin/vet_form.html', action='Edit', contact=contact)
