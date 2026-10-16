import io
from tests.conftest import create_dummy_image
from app.services.plant_service import validate_image_file, perform_agronomic_assessment
from werkzeug.datastructures import FileStorage


def test_image_validation_valid():
    img_io = create_dummy_image()
    fs = FileStorage(stream=img_io, filename='leaf_test.jpg', content_type='image/jpeg')
    is_valid, err, name = validate_image_file(fs)
    assert is_valid is True
    assert err is None
    assert name == 'leaf_test.jpg'


def test_image_validation_invalid_extension():
    fake_io = io.BytesIO(b'dummy script content')
    fs = FileStorage(stream=fake_io, filename='exploit.sh', content_type='text/x-shellscript')
    is_valid, err, name = validate_image_file(fs)
    assert is_valid is False
    assert 'not supported' in err


def test_image_validation_corrupted_file():
    corrupt_io = io.BytesIO(b'not a genuine image file header')
    fs = FileStorage(stream=corrupt_io, filename='fake.jpg', content_type='image/jpeg')
    is_valid, err, name = validate_image_file(fs)
    assert is_valid is False
    assert 'not a valid' in err


def test_plant_assessment_rice_blast(client):
    img_io = create_dummy_image()
    res = client.post('/plant/checker', data={
        'crop_type': 'Rice',
        'growth_stage': 'Vegetative',
        'affected_parts': 'Leaves',
        'symptoms': ['spindle boat shaped leaf spots'],
        'symptoms_notes': 'spots have grey centre and brown border',
        'plant_image': (img_io, 'leaf.jpg')
    }, content_type='multipart/form-data')
    assert res.status_code == 200
    assert b'Rice Blast' in res.data
    assert b'ICAR' in res.data
    assert b'Configuration Notice' in res.data or b'unconfigured' in res.data


def test_plant_assessment_tomato_early_blight(client):
    res = client.post('/plant/checker', data={
        'crop_type': 'Tomato',
        'growth_stage': 'Fruiting',
        'affected_parts': 'Leaves',
        'symptoms': ['concentric target board brown rings'],
        'symptoms_notes': 'circular target rings on lower leaves'
    })
    assert res.status_code == 200
    assert b'Early Blight' in res.data
    assert b'Alternaria' in res.data
    assert b'Trichoderma' in res.data
