"""
Knowledge Base Service.
Manages verified agronomic, veterinary, and fertilizer management guidelines
sourced from official Indian research institutions (ICAR, IVRI, State Agricultural Universities).
"""
from app import db
from app.models import KnowledgeArticle


def get_articles(category=None, query=None, active_only=True):
    """Retrieves articles filtered by category and search terms."""
    q = KnowledgeArticle.query
    if active_only:
        q = q.filter_by(is_active=True)
    if category and category != 'all':
        q = q.filter_by(category=category)
    if query and query.strip():
        term = f"%{query.strip()}%"
        q = q.filter(
            (KnowledgeArticle.title.ilike(term)) |
            (KnowledgeArticle.crop_or_animal.ilike(term)) |
            (KnowledgeArticle.symptoms_description.ilike(term)) |
            (KnowledgeArticle.management_practices.ilike(term))
        )
    return q.order_by(KnowledgeArticle.category, KnowledgeArticle.title).all()


def get_article_by_id(article_id):
    """Fetch article by primary key."""
    return KnowledgeArticle.query.get(article_id)


def get_fertilizer_guides():
    """Returns verified fertilizer schedules for major Indian crops."""
    return KnowledgeArticle.query.filter_by(category='fertilizer', is_active=True).all()


def get_crop_treatments(crop_name=None):
    """Returns verified plant disease/pest treatments."""
    q = KnowledgeArticle.query.filter(
        KnowledgeArticle.category.in_(['crop_disease', 'pest', 'treatment']),
        KnowledgeArticle.is_active == True
    )
    if crop_name and crop_name.strip():
        q = q.filter(KnowledgeArticle.crop_or_animal.ilike(f"%{crop_name.strip()}%"))
    return q.all()


def get_animal_conditions(species=None):
    """Returns verified animal health conditions."""
    q = KnowledgeArticle.query.filter_by(category='animal_health', is_active=True)
    if species and species.strip():
        q = q.filter(KnowledgeArticle.crop_or_animal.ilike(f"%{species.strip()}%"))
    return q.all()
