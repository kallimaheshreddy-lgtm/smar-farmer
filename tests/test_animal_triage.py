import pytest
from app.services.animal_service import evaluate_animal_triage


def test_triage_emergency_downer_recumbent():
    eval_res = evaluate_animal_triage(
        species='Cow',
        standing_status='unable',
        symptoms_selected='cannot stand downer cow',
        appetite='stopped'
    )
    assert eval_res['urgency_level'] == 'emergency'
    assert eval_res['requires_immediate_vet'] is True
    assert '1962' in eval_res['helpline']
    assert 'DO NOT DRENCH' in eval_res['what_not_to_do']


def test_triage_emergency_severe_bloat():
    eval_res = evaluate_animal_triage(
        species='Buffalo',
        symptoms_selected='severe bloat tympany distended stomach',
        breathing_status='distress'
    )
    assert eval_res['urgency_level'] == 'emergency'
    assert eval_res['requires_immediate_vet'] is True
    assert 'CALL A VETERINARIAN' in eval_res['interim_guidance']


def test_triage_urgent_off_feed_fever():
    eval_res = evaluate_animal_triage(
        species='Goat',
        appetite='stopped',
        temperature_status='high_fever',
        behavior='dull'
    )
    assert eval_res['urgency_level'] == 'urgent'
    assert eval_res['requires_immediate_vet'] is False
    assert '12' in eval_res['urgency_title']


def test_triage_monitor_mild_signs():
    eval_res = evaluate_animal_triage(
        species='Sheep',
        appetite='normal',
        behavior='alert',
        standing_status='normal',
        symptoms_selected='minor scrape on leg'
    )
    assert eval_res['urgency_level'] == 'monitor'
    assert 'MONITOR' in eval_res['urgency_title']


def test_triage_endpoint_via_client(client):
    res = client.post('/animal/triage', data={
        'species': 'Cow',
        'age_approx': '4 years',
        'appetite': 'stopped',
        'behavior': 'dull',
        'standing_status': 'unable',
        'symptoms': ['unable to stand downer', 'foaming at mouth']
    })
    assert res.status_code == 200
    assert b'CRITICAL EMERGENCY' in res.data
    assert b'1962' in res.data
    assert b'DO NOT' in res.data


def test_animal_quick_solve_with_photo(client):
    from tests.conftest import create_dummy_image
    img_io = create_dummy_image()
    res = client.post('/animal/quick-solve', data={
        'species': 'Cow',
        'animal_image': (img_io, 'cow_skin.jpg')
    }, content_type='multipart/form-data', follow_redirects=True)
    assert res.status_code == 200
    assert b'1962' in res.data
    assert b'DO NOT' in res.data

