import pytest
from app.models import KnowledgeArticle
from app.services.knowledge_service import get_articles


def test_knowledge_articles_source_and_date(app):
    with app.app_context():
        articles = get_articles()
        assert len(articles) > 0
        for a in articles:
            assert a.source_institution is not None and len(a.source_institution) > 0
            assert a.last_reviewed_date is not None and len(a.last_reviewed_date) > 0


def test_knowledge_search(client):
    res = client.get('/knowledge/?q=Blast')
    assert res.status_code == 200
    assert b'Rice Blast' in res.data


def test_admin_authorization_required(client):
    # Unauthenticated visitor blocked
    res = client.get('/admin/', follow_redirects=True)
    assert b'Please log in' in res.data or b'Login' in res.data


def test_non_admin_forbidden_from_admin_portal(auth_client):
    # Regular farmer logged in
    res = auth_client.get('/admin/', follow_redirects=True)
    assert b'Administrator privileges required' in res.data


def test_admin_portal_access_and_toggle(app, admin_client):
    res = admin_client.get('/admin/')
    assert res.status_code == 200
    assert b'Administrator Control Portal' in res.data

    # Toggle knowledge article
    with app.app_context():
        art = KnowledgeArticle.query.first()
        art_id = art.id
        initial_status = art.is_active

    toggle_res = admin_client.post(f'/admin/knowledge/toggle/{art_id}', follow_redirects=True)
    assert toggle_res.status_code == 200

    with app.app_context():
        art = KnowledgeArticle.query.get(art_id)
        assert art.is_active != initial_status
