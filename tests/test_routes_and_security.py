from flask import session


def test_healthz_endpoint(client):
    res = client.get('/healthz')
    assert res.status_code == 200
    json_data = res.get_json()
    assert json_data['status'] == 'healthy'
    assert json_data['service'] == 'Smart Farmer AI'
    assert 'en' in json_data['supported_locales']


def test_language_switcher(client):
    res = client.get('/set_language/te', follow_redirects=True)
    assert res.status_code == 200
    with client.session_transaction() as sess:
        assert sess['locale'] == 'te'

    res_hi = client.get('/set_language/hi', follow_redirects=True)
    assert res_hi.status_code == 200
    with client.session_transaction() as sess:
        assert sess['locale'] == 'hi'


def test_custom_404_page(client):
    res = client.get('/non-existent-page-url-404')
    assert res.status_code == 404
    assert b'404' in res.data
    assert b'Page Not Found' in res.data


def test_guides_and_directory_endpoints(client):
    assert client.get('/knowledge/crop-treatments').status_code == 200
    assert client.get('/knowledge/fertilizer-guide').status_code == 200
    assert client.get('/vets/').status_code == 200
    assert client.get('/weather/').status_code == 200
