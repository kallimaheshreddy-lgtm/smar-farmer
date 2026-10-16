import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(80), nullable=True, default='Telangana')
    district = db.Column(db.String(80), nullable=True, default='Warangal')
    preferred_language = db.Column(db.String(10), default='en')
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    farms = db.relationship('Farm', backref='owner', lazy=True, cascade='all, delete-orphan')
    crops = db.relationship('Crop', backref='user', lazy=True, cascade='all, delete-orphan')
    activities = db.relationship('FarmActivity', backref='user', lazy=True, cascade='all, delete-orphan')
    livestock = db.relationship('Livestock', backref='user', lazy=True, cascade='all, delete-orphan')
    vet_visits = db.relationship('VetVisit', backref='user', lazy=True, cascade='all, delete-orphan')
    plant_assessments = db.relationship('PlantAssessment', backref='user', lazy=True)
    animal_triages = db.relationship('AnimalTriageRecord', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email} ({self.name})>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Farm(db.Model):
    __tablename__ = 'farms'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    total_area_acres = db.Column(db.Float, default=1.0)
    soil_type = db.Column(db.String(80), default='Black Cotton Soil')
    irrigation_source = db.Column(db.String(100), default='Borewell')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    crops = db.relationship('Crop', backref='farm', lazy=True)


class Crop(db.Model):
    __tablename__ = 'crops'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=True)
    name = db.Column(db.String(120), nullable=False)
    variety = db.Column(db.String(120), nullable=True)
    field_name = db.Column(db.String(120), default='Main Plot')
    area_acres = db.Column(db.Float, default=1.0)
    planting_date = db.Column(db.Date, nullable=True)
    expected_harvest_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default='Growing')  # Growing, Flowering, Harvesting, Harvested
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    activities = db.relationship('FarmActivity', backref='crop', lazy=True, cascade='all, delete-orphan')
    assessments = db.relationship('PlantAssessment', backref='crop', lazy=True)


class FarmActivity(db.Model):
    __tablename__ = 'farm_activities'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=True)
    activity_type = db.Column(db.String(80), nullable=False)  # Irrigation, Fertilizer, Pest Control, Harvest, Expense
    activity_date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.String(80), nullable=True)
    cost = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Livestock(db.Model):
    __tablename__ = 'livestock'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    tag_id = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    species = db.Column(db.String(60), nullable=False)  # Cow, Buffalo, Goat, Sheep, Poultry, Other
    breed = db.Column(db.String(100), nullable=True)
    age_months = db.Column(db.Integer, default=12)
    gender = db.Column(db.String(20), default='Female')
    health_status = db.Column(db.String(50), default='Healthy')  # Healthy, Observation, Sick, Recovering
    reproductive_status = db.Column(db.String(60), default='Lactating')  # Lactating, Pregnant, Dry, Calf/Kid
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vet_visits = db.relationship('VetVisit', backref='animal', lazy=True, cascade='all, delete-orphan')
    triages = db.relationship('AnimalTriageRecord', backref='animal', lazy=True)


class VetVisit(db.Model):
    __tablename__ = 'vet_visits'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    livestock_id = db.Column(db.Integer, db.ForeignKey('livestock.id'), nullable=True)
    visit_date = db.Column(db.Date, default=datetime.utcnow)
    vet_name = db.Column(db.String(120), nullable=False)
    clinic_name = db.Column(db.String(150), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    reason = db.Column(db.String(200), nullable=False)
    diagnosis_notes = db.Column(db.Text, nullable=True)
    advice_given = db.Column(db.Text, nullable=True)
    follow_up_date = db.Column(db.Date, nullable=True)
    cost = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PlantAssessment(db.Model):
    __tablename__ = 'plant_assessments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=True)
    crop_type = db.Column(db.String(100), nullable=False)
    growth_stage = db.Column(db.String(80), nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    symptoms_selected = db.Column(db.Text, nullable=True)
    symptoms_notes = db.Column(db.Text, nullable=True)
    detected_issue = db.Column(db.String(200), nullable=False)
    confidence = db.Column(db.String(30), default='N/A')
    assessment_mode = db.Column(db.String(60), default='Agronomic Screening')  # AI Model or Agronomic Screening
    reasons_supporting = db.Column(db.Text, nullable=True)
    alternative_causes = db.Column(db.Text, nullable=True)
    recommended_steps = db.Column(db.Text, nullable=True)
    safety_precautions = db.Column(db.Text, nullable=True)
    source_institution = db.Column(db.String(255), nullable=True)
    review_date = db.Column(db.String(50), nullable=True)
    requires_expert_visit = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AnimalTriageRecord(db.Model):
    __tablename__ = 'animal_triage_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    livestock_id = db.Column(db.Integer, db.ForeignKey('livestock.id'), nullable=True)
    species = db.Column(db.String(60), nullable=False)
    age_approx = db.Column(db.String(50), nullable=True)
    symptoms_selected = db.Column(db.Text, nullable=True)
    symptoms_notes = db.Column(db.Text, nullable=True)
    appetite = db.Column(db.String(60), nullable=True)
    behavior = db.Column(db.String(60), nullable=True)
    temperature_status = db.Column(db.String(60), nullable=True)
    breathing_status = db.Column(db.String(60), nullable=True)
    standing_status = db.Column(db.String(60), nullable=True)
    urgency_level = db.Column(db.String(40), nullable=False)  # emergency, urgent, monitor
    immediate_guidance = db.Column(db.Text, nullable=False)
    what_not_to_do = db.Column(db.Text, nullable=True)
    requires_immediate_vet = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class KnowledgeArticle(db.Model):
    __tablename__ = 'knowledge_articles'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(60), nullable=False, index=True)  # crop_disease, pest, treatment, fertilizer, animal_health
    title = db.Column(db.String(250), nullable=False)
    crop_or_animal = db.Column(db.String(100), nullable=True, index=True)
    symptoms_description = db.Column(db.Text, nullable=True)
    management_practices = db.Column(db.Text, nullable=False)
    organic_options = db.Column(db.Text, nullable=True)
    safety_precautions = db.Column(db.Text, nullable=True)
    source_institution = db.Column(db.String(255), nullable=False)
    last_reviewed_date = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VetContact(db.Model):
    __tablename__ = 'vet_contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    contact_type = db.Column(db.String(100), default='Govt Veterinary Dispensary')
    state = db.Column(db.String(80), nullable=False, index=True)
    district = db.Column(db.String(80), nullable=False, index=True)
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(50), nullable=False)
    emergency_phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AnimalAssessment(db.Model):
    __tablename__ = 'animal_assessments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    animal_type = db.Column(db.String(80), nullable=False)
    age_months = db.Column(db.Integer, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    symptoms = db.Column(db.Text, nullable=False)
    duration_days = db.Column(db.Integer, nullable=True)
    eating_behavior = db.Column(db.String(120), nullable=True)
    drinking_behavior = db.Column(db.String(120), nullable=True)
    milk_change = db.Column(db.String(120), nullable=True)
    pregnancy_status = db.Column(db.String(80), nullable=True)
    temperature_c = db.Column(db.Float, nullable=True)
    triage_category = db.Column(db.String(30), default='routine')
    advice = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TreatmentRecord(db.Model):
    __tablename__ = 'treatment_records'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    target_name = db.Column(db.String(150), nullable=False)
    problem = db.Column(db.String(200), nullable=False)
    recommended_action = db.Column(db.Text, nullable=True)
    evidence_source = db.Column(db.String(255), nullable=True)
    verification_date = db.Column(db.Date, nullable=True)
    safety_precautions = db.Column(db.Text, nullable=True)
    when_to_contact_professional = db.Column(db.Text, nullable=True)
    is_example = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FarmExpense(db.Model):
    __tablename__ = 'farm_expenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    expense_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class WeatherRecord(db.Model):
    __tablename__ = 'weather_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    location = db.Column(db.String(150), nullable=True)
    temperature_c = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    rainfall_forecast_mm = db.Column(db.Float, nullable=True)
    alert_text = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(150), default='Not configured')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class KnowledgeBaseEntry(db.Model):
    __tablename__ = 'knowledge_base_entries'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    target_name = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    evidence_source = db.Column(db.String(255))
    verification_date = db.Column(db.Date)
    is_example = db.Column(db.Boolean, default=True)
    is_outdated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


def seed_example_knowledge(db_session):
    if KnowledgeBaseEntry.query.first():
        return

    samples = [
        {
            'category': 'crop',
            'target_name': 'Tomato',
            'subject': 'Leaf spot management',
            'summary': 'Example advisory only. Inspect the crop and verify with local extension services before applying any treatment.',
            'recommendation': 'Remove affected leaves, avoid overhead watering, and contact local agricultural support if symptoms spread rapidly.',
            'evidence_source': 'Example extension guidance; requires expert verification.',
            'verification_date': datetime.utcnow().date(),
            'is_example': True,
        },
        {
            'category': 'animal',
            'target_name': 'Cow',
            'subject': 'Reduced feeding',
            'summary': 'Example advisory only. Reduced feeding and weakness require timely veterinary review.',
            'recommendation': 'Isolate the animal, provide clean water, and consult a qualified veterinarian promptly.',
            'evidence_source': 'Example veterinary guidance; requires professional review.',
            'verification_date': datetime.utcnow().date(),
            'is_example': True,
        },
    ]

    for item in samples:
        db_session.add(KnowledgeBaseEntry(**item))
    db_session.commit()

