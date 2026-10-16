import pytest
from app import db
from app.models import User, Crop, Livestock


def test_crop_data_isolation(app, client):
    # Farmer 1 creates crop
    client.post('/auth/login', data={'email': 'farmer1@test.com', 'password': 'FarmerPass123'})
    client.post('/farm/crop/add', data={
        'name': 'Paddy Samba',
        'variety': 'BPT 5204',
        'field_name': 'Plot A',
        'area_acres': '2.5',
        'status': 'Growing'
    }, follow_redirects=True)

    with app.app_context():
        u1 = User.query.filter_by(email='farmer1@test.com').first()
        crop = Crop.query.filter_by(user_id=u1.id).first()
        assert crop is not None
        crop_id = crop.id

    client.get('/auth/logout')

    # Farmer 2 logs in and attempts to edit/delete Farmer 1's crop
    client.post('/auth/login', data={'email': 'farmer2@test.com', 'password': 'FarmerPass123'})
    edit_res = client.get(f'/farm/crop/edit/{crop_id}')
    assert edit_res.status_code == 404

    del_res = client.post(f'/farm/crop/delete/{crop_id}')
    assert del_res.status_code == 404


def test_livestock_data_isolation(app, client):
    # Farmer 1 adds livestock
    client.post('/auth/login', data={'email': 'farmer1@test.com', 'password': 'FarmerPass123'})
    client.post('/livestock/add', data={
        'tag_id': 'COW-PRIVATE-01',
        'name': 'Gauri',
        'species': 'Cow',
        'breed': 'Gir',
        'age_months': '30',
        'gender': 'Female',
        'health_status': 'Healthy',
        'reproductive_status': 'Lactating'
    }, follow_redirects=True)

    with app.app_context():
        u1 = User.query.filter_by(email='farmer1@test.com').first()
        cow = Livestock.query.filter_by(user_id=u1.id, tag_id='COW-PRIVATE-01').first()
        assert cow is not None
        cow_id = cow.id

    client.get('/auth/logout')

    # Farmer 2 logs in and tries to modify Farmer 1's livestock
    client.post('/auth/login', data={'email': 'farmer2@test.com', 'password': 'FarmerPass123'})
    edit_res = client.get(f'/livestock/edit/{cow_id}')
    assert edit_res.status_code == 404

    del_res = client.post(f'/livestock/delete/{cow_id}')
    assert del_res.status_code == 404
