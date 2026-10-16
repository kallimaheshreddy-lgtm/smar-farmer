from app.services.weather_service import (
    get_weather_data,
    generate_farm_advisories,
    MAJOR_INDIAN_AGRICULTURAL_DISTRICTS
)


def test_weather_missing_api_key_no_fabrication():
    # Calling without API key
    data = get_weather_data('Warangal, Telangana')
    assert data['configured'] is False
    assert 'WEATHER_API_KEY' in data['notice']
    assert 'openweathermap.org' in data['setup_guide']
    # Ensures we do not fabricate random temperatures
    assert 'temperature' not in data
    assert len(data['advisories']) > 0


def test_weather_spray_and_humidity_advisories():
    # Test high wind speed
    adv_wind = generate_farm_advisories(temp=28, humidity=60, wind_speed=6.0)
    wind_alert = next((a for a in adv_wind if a['category'] == 'Spraying Warning'), None)
    assert wind_alert is not None
    assert 'Postpone pesticide' in wind_alert['message']

    # Test calm wind speed
    adv_calm = generate_farm_advisories(temp=28, humidity=60, wind_speed=2.0)
    spray_ok = next((a for a in adv_calm if a['category'] == 'Foliar Spray Window'), None)
    assert spray_ok is not None
    assert 'suitable' in spray_ok['message']

    # Test high humidity disease risk
    adv_hum = generate_farm_advisories(temp=25, humidity=82, wind_speed=2.0)
    hum_alert = next((a for a in adv_hum if a['category'] == 'Disease Surveillance Risk'), None)
    assert hum_alert is not None
    assert 'High relative humidity' in hum_alert['message']


def test_weather_endpoint_client(client):
    res = client.get('/weather/?district=Warangal, Telangana')
    assert res.status_code == 200
    assert b'Agro-Climatic Weather' in res.data
    assert b'Warangal' in res.data
