import pytest
from app.models import User


def test_user_registration_success(client):
    res = client.post('/auth/register', data={
        'name': 'New Farmer',
        'email': 'newfarmer@test.com',
        'phone': '9848033333',
        'state': 'Telangana',
        'district': 'Warangal',
        'language': 'te',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Account registered successfully' in res.data
    user = User.query.filter_by(email='newfarmer@test.com').first()
    assert user is not None
    assert user.name == 'New Farmer'
    assert user.preferred_language == 'te'


def test_registration_password_mismatch(client):
    res = client.post('/auth/register', data={
        'name': 'Mismatch Farmer',
        'email': 'mismatch@test.com',
        'password': 'password123',
        'confirm_password': 'password456'
    }, follow_redirects=True)
    assert b'Passwords do not match' in res.data


def test_registration_duplicate_email(client):
    res = client.post('/auth/register', data={
        'name': 'Duplicate Farmer',
        'email': 'farmer1@test.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert b'already registered' in res.data


def test_login_success(client):
    res = client.post('/auth/login', data={
        'email': 'farmer1@test.com',
        'password': 'FarmerPass123'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Farmer One' in res.data


def test_login_invalid_password(client):
    res = client.post('/auth/login', data={
        'email': 'farmer1@test.com',
        'password': 'WrongPassword'
    }, follow_redirects=True)
    assert b'Invalid' in res.data


def test_login_with_mobile_number(client):
    res = client.post('/auth/login', data={
        'phone': '9848011111',
        'password': 'FarmerPass123'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Farmer One' in res.data


def test_login_with_only_mobile_number_no_password(client):
    res = client.post('/auth/login', data={
        'phone': '9848011111'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Farmer One' in res.data



def test_registration_with_only_mobile_number(client):
    res = client.post('/auth/register', data={
        'name': 'Mobile Only Farmer',
        'phone': '9848077777',
        'password': '1234',
        'confirm_password': '1234'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Account registered successfully' in res.data
    user = User.query.filter_by(phone='9848077777').first()
    assert user is not None
    assert user.name == 'Mobile Only Farmer'


def test_registration_invalid_phone(client):
    res = client.post('/auth/register', data={
        'name': 'Bad Phone Farmer',
        'phone': '12345',
        'password': '1234',
        'confirm_password': '1234'
    }, follow_redirects=True)
    assert b'valid 10-digit' in res.data


def test_logout(auth_client):
    res = auth_client.get('/auth/logout', follow_redirects=True)
    assert res.status_code == 200
    assert b'logged out' in res.data

