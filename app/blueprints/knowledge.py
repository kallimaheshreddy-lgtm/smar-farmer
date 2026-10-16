from flask import Blueprint, render_template, request
from app.models import KnowledgeArticle
from app.services.knowledge_service import (
    get_articles,
    get_article_by_id,
    get_fertilizer_guides,
    get_crop_treatments
)

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/knowledge')


@knowledge_bp.route('/')
def index():
    """Searchable agricultural and veterinary knowledge repository."""
    category = request.args.get('category', 'all')
    query = request.args.get('q', '').strip()
    articles = get_articles(category=category, query=query)
    
    return render_template(
        'knowledge/index.html',
        articles=articles,
        current_category=category,
        query=query
    )


@knowledge_bp.route('/crop-treatments')
def crop_treatments():
    """Dedicated guide for verified crop disease and pest management."""
    crop_filter = request.args.get('crop', '').strip()
    treatments = get_crop_treatments(crop_name=crop_filter)
    return render_template('knowledge/crop_treatments.html', treatments=treatments, crop_filter=crop_filter)


@knowledge_bp.route('/fertilizer-guide')
def fertilizer_guide():
    """Dedicated scientific fertilizer schedule and nutrient guide."""
    guides = get_fertilizer_guides()
    return render_template('knowledge/fertilizer_guide.html', guides=guides)


@knowledge_bp.route('/article/<int:article_id>')
def view_article(article_id):
    """Detailed view of an official agronomic or veterinary article."""
    article = KnowledgeArticle.query.get_or_404(article_id)
    return render_template('knowledge/article.html', article=article)
