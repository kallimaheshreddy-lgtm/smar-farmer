import pytest

from app import create_app
from config import normalize_database_url


@pytest.mark.parametrize('secret_key', [None, '', '   '])
def test_production_requires_secret_key(monkeypatch, secret_key):
    if secret_key is None:
        monkeypatch.delenv('SECRET_KEY', raising=False)
    else:
        monkeypatch.setenv('SECRET_KEY', secret_key)

    with pytest.raises(RuntimeError, match='SECRET_KEY must be set'):
        create_app('production')


def test_production_uses_configured_secret_key(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'configured-production-secret')

    app = create_app('production')

    assert app.config['SECRET_KEY'] == 'configured-production-secret'
    assert app.config['SESSION_COOKIE_SECURE'] is True


@pytest.mark.parametrize(
    ('database_url', 'expected_url'),
    [
        ('postgres://user:pass@host/database', 'postgresql+psycopg://user:pass@host/database'),
        ('postgresql://user:pass@host/database', 'postgresql+psycopg://user:pass@host/database'),
        ('sqlite:///local.db', 'sqlite:///local.db'),
    ],
)
def test_database_url_normalization(database_url, expected_url):
    assert normalize_database_url(database_url) == expected_url
