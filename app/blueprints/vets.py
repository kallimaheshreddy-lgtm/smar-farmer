from flask import Blueprint, render_template, request
from app.models import VetContact

vets_bp = Blueprint('vets', __name__, url_prefix='/vets')


@vets_bp.route('/')
def index():
    """Directory of verified veterinary hospitals, polyclinics, and KVK centers."""
    state_filter = request.args.get('state', '').strip()
    district_filter = request.args.get('district', '').strip()
    
    query = VetContact.query.filter_by(is_active=True)
    if state_filter and state_filter != 'all':
        query = query.filter_by(state=state_filter)
    if district_filter:
        query = query.filter(VetContact.district.ilike(f"%{district_filter}%"))
        
    contacts = query.order_by(VetContact.state, VetContact.district, VetContact.name).all()
    
    # Get distinct states for dropdown filter
    all_states = [s[0] for s in VetContact.query.with_entities(VetContact.state).distinct().all()]
    
    return render_template(
        'vets/index.html',
        contacts=contacts,
        states=sorted(all_states),
        selected_state=state_filter,
        district_query=district_filter
    )
