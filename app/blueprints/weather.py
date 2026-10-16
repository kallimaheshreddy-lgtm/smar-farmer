from flask import Blueprint, render_template, request
from flask_login import current_user
from app.services.weather_service import (
    get_weather_data,
    MAJOR_INDIAN_AGRICULTURAL_DISTRICTS
)

weather_bp = Blueprint('weather', __name__, url_prefix='/weather')


@weather_bp.route('/', methods=['GET'])
def index():
    """Weather and agro-climatic advisory dashboard."""
    # Default to user's registered district or Warangal, Telangana
    default_district = 'Warangal, Telangana'
    if current_user.is_authenticated and current_user.district:
        candidate = f"{current_user.district}, {current_user.state or 'Telangana'}"
        if candidate in MAJOR_INDIAN_AGRICULTURAL_DISTRICTS:
            default_district = candidate
            
    selected_district = request.args.get('district', default_district)
    if selected_district not in MAJOR_INDIAN_AGRICULTURAL_DISTRICTS:
        selected_district = default_district
        
    lat_str = request.args.get('lat')
    lon_str = request.args.get('lon')
    lat = float(lat_str) if lat_str else None
    lon = float(lon_str) if lon_str else None
    
    weather_info = get_weather_data(selected_district, lat=lat, lon=lon)
    
    return render_template(
        'weather/index.html',
        weather=weather_info,
        districts=list(MAJOR_INDIAN_AGRICULTURAL_DISTRICTS.keys()),
        selected_district=selected_district
    )
