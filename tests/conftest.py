import io
import pytest
from PIL import Image
from app import create_app, db
from app.models import User, KnowledgeArticle, VetContact


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # Seed test admin & farmer
        admin = User(
            name='Test Admin',
            email='admin@test.com',
            phone='18001801551',
            is_admin=True
        )
        admin.set_password('AdminPass123')
        db.session.add(admin)

        user1 = User(
            name='Farmer One',
            email='farmer1@test.com',
            phone='9848011111',
            is_admin=False
        )
        user1.set_password('FarmerPass123')
        db.session.add(user1)

        user2 = User(
            name='Farmer Two',
            email='farmer2@test.com',
            phone='9848022222',
            is_admin=False
        )
        user2.set_password('FarmerPass123')
        db.session.add(user2)

        # Seed test knowledge article
        art = KnowledgeArticle(
            category='crop_disease',
            title='Rice Blast Control Test',
            crop_or_animal='Rice',
            symptoms_description='Spindle spots on leaves',
            management_practices='Spray Pseudomonas fluorescens @ 2.5 kg/ha',
            organic_options='Cow dung extract',
            safety_precautions='Wear gloves and face mask',
            source_institution='ICAR-IIRR Hyderabad',
            last_reviewed_date='August 2026',
            is_active=True
        )
        db.session.add(art)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(app, client):
    """Client authenticated as Farmer One"""
    client.post('/auth/login', data={
        'email': 'farmer1@test.com',
        'password': 'FarmerPass123'
    })
    return client


@pytest.fixture
def admin_client(app, client):
    """Client authenticated as Test Admin"""
    client.post('/auth/login', data={
        'email': 'admin@test.com',
        'password': 'AdminPass123'
    })
    return client


def create_dummy_image():
    """Generates a valid in-memory JPEG image via Pillow for testing."""
    file_bytes = io.BytesIO()
    img = Image.new('RGB', (100, 100), color='green')
    img.save(file_bytes, format='JPEG')
    file_bytes.seek(0)
    return file_bytes
