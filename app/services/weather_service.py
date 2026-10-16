"""
Weather and Agro-Climatic Advisory Service.
Supports OpenWeatherMap API with graceful fallback, clear setup guidance,
manual district/region selector across major Indian agricultural zones,
and actionable agricultural spray/irrigation advisories.
"""
import os
import requests

MAJOR_INDIAN_AGRICULTURAL_DISTRICTS = {
    'Warangal, Telangana': {'lat': 17.9784, 'lon': 79.5941, 'state': 'Telangana', 'zone': 'Southern Telangana Agro-Climatic Zone'},
    'Guntur, Andhra Pradesh': {'lat': 16.3067, 'lon': 80.4365, 'state': 'Andhra Pradesh', 'zone': 'Krishna-Godavari Coastal Zone'},
    'Pune, Maharashtra': {'lat': 18.5204, 'lon': 73.8567, 'state': 'Maharashtra', 'zone': 'Western Maharashtra Plains Zone'},
    'Ludhiana, Punjab': {'lat': 30.9010, 'lon': 75.8573, 'state': 'Punjab', 'zone': 'Central Plain Agro-Climatic Zone'},
    'Karnal, Haryana': {'lat': 29.6857, 'lon': 76.9905, 'state': 'Haryana', 'zone': 'Eastern Agricultural Zone'},
    'Varanasi, Uttar Pradesh': {'lat': 25.3176, 'lon': 82.9739, 'state': 'Uttar Pradesh', 'zone': 'Eastern Plain Zone'},
    'Coimbatore, Tamil Nadu': {'lat': 11.0168, 'lon': 76.9558, 'state': 'Tamil Nadu', 'zone': 'Western Agricultural Zone'},
    'Dharwad, Karnataka': {'lat': 15.4589, 'lon': 75.0078, 'state': 'Karnataka', 'zone': 'Northern Transition Zone'},
    'Indore, Madhya Pradesh': {'lat': 22.7196, 'lon': 75.8577, 'state': 'Madhya Pradesh', 'zone': 'Malwa Plateau Zone'},
    'Anand, Gujarat': {'lat': 22.5645, 'lon': 72.9289, 'state': 'Gujarat', 'zone': 'Middle Gujarat Agro-Climatic Zone'},
    'Jaipur, Rajasthan': {'lat': 26.9124, 'lon': 75.7873, 'state': 'Rajasthan', 'zone': 'Semi-Arid Eastern Plain Zone'},
    'Patna, Bihar': {'lat': 25.5941, 'lon': 85.1376, 'state': 'Bihar', 'zone': 'South Bihar Alluvial Plain Zone'}
}


def get_weather_data(district_name='Warangal, Telangana', lat=None, lon=None):
    """
    Fetches real-time weather from OpenWeatherMap if WEATHER_API_KEY is configured.
    If unconfigured or if API call fails, transparently returns configuration guide
    and agro-climatic baseline advisory for the selected location without inventing numbers.
    """
    api_key = os.environ.get('WEATHER_API_KEY')
    
    # Resolve coords
    district_info = MAJOR_INDIAN_AGRICULTURAL_DISTRICTS.get(district_name, MAJOR_INDIAN_AGRICULTURAL_DISTRICTS['Warangal, Telangana'])
    target_lat = lat if lat is not None else district_info['lat']
    target_lon = lon if lon is not None else district_info['lon']
    
    if api_key and api_key.strip():
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={target_lat}&lon={target_lon}&appid={api_key}&units=metric"
            resp = requests.get(url, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                temp = data.get('main', {}).get('temp')
                humidity = data.get('main', {}).get('humidity')
                wind_speed = data.get('wind', {}).get('speed')
                description = data.get('weather', [{}])[0].get('description', 'Clear')
                
                advisories = generate_farm_advisories(temp, humidity, wind_speed)
                return {
                    'configured': True,
                    'location_name': district_name,
                    'zone': district_info.get('zone'),
                    'temperature': temp,
                    'humidity': humidity,
                    'wind_speed': wind_speed,
                    'description': description.capitalize(),
                    'source': 'Live OpenWeatherMap API',
                    'advisories': advisories
                }
            else:
                return {
                    'configured': False,
                    'api_error': f"Weather API error (HTTP {resp.status_code}): Please verify your API key.",
                    'location_name': district_name,
                    'zone': district_info.get('zone'),
                    'setup_guide': (
                        "To view real-time automated weather forecasts:\n"
                        "1. Sign up for a free API key at https://openweathermap.org/\n"
                        "2. Add WEATHER_API_KEY=your_key_here to your environment or .env file.\n"
                        "3. Restart the application."
                    ),
                    'advisories': generate_district_baseline_advisory(district_name)
                }
        except Exception as e:
            return {
                'configured': False,
                'api_error': f"Could not reach Weather service: {str(e)}",
                'location_name': district_name,
                'zone': district_info.get('zone'),
                'setup_guide': "Check your internet connection and verify WEATHER_API_KEY.",
                'advisories': generate_district_baseline_advisory(district_name)
            }
    
    # Missing API Key - explicit, transparent notice (NO fabrication)
    return {
        'configured': False,
        'location_name': district_name,
        'zone': district_info.get('zone'),
        'notice': 'Live weather feed requires an OpenWeatherMap API key (WEATHER_API_KEY). Showing regional agro-climatic advisory.',
        'setup_guide': (
            "How to configure Live Weather:\n"
            "1. Visit https://openweathermap.org/api and create a free account.\n"
            "2. Generate a free API key (Current Weather Data).\n"
            "3. Set the key in your .env file: WEATHER_API_KEY=your_actual_key\n"
            "4. Restart the web server. Forecasts will automatically update."
        ),
        'advisories': generate_district_baseline_advisory(district_name)
    }


def generate_farm_advisories(temp, humidity, wind_speed):
    """Produces practical farming advisories based on real meteorological parameters."""
    adv = []
    
    # Spraying advice
    if wind_speed and wind_speed > 4.5:
        adv.append({
            'category': 'Spraying Warning',
            'alert_type': 'warning',
            'message': f"Wind speed is {wind_speed} m/s. Postpone pesticide/foliar sprays to prevent chemical drift onto neighbouring crops and loss of efficacy."
        })
    else:
        adv.append({
            'category': 'Foliar Spray Window',
            'alert_type': 'success',
            'message': "Wind speed is calm and suitable for morning foliar nutrition or bio-agent spray operations."
        })
        
    # Humidity & Disease Risk
    if humidity and humidity > 75:
        adv.append({
            'category': 'Disease Surveillance Risk',
            'alert_type': 'warning',
            'message': f"High relative humidity ({humidity}%). Favorable for fungal pathogens like blast, downy mildew, and blight. Scout crops closely for early symptoms."
        })
    elif humidity and humidity < 35:
        adv.append({
            'category': 'Evaporation & Soil Moisture',
            'alert_type': 'info',
            'message': f"Low humidity ({humidity}%) and dry air accelerate soil evaporation. Check soil moisture and schedule irrigation for sensitive crops."
        })
        
    # Temperature & Livestock Care
    if temp and temp > 36:
        adv.append({
            'category': 'Heat Stress Caution for Livestock',
            'alert_type': 'danger',
            'message': f"High ambient temperature ({temp}°C). Provide shaded housing, fresh cool drinking water, and electrolytes. Avoid moving or working bullocks during midday (11 AM - 3 PM)."
        })
    elif temp and temp < 14:
        adv.append({
            'category': 'Cold Shelter Advisory',
            'alert_type': 'info',
            'message': f"Cool night temperatures ({temp}°C). Protect young calves, kids, and poultry chicks from cold night drafts using curtains/straw bedding."
        })
        
    return adv


def generate_district_baseline_advisory(district_name):
    """Provides regional agronomic advisory when live sensor/API keys are unconfigured."""
    return [
        {
            'category': 'Seasonal Irrigation Planning',
            'alert_type': 'info',
            'message': f"In {district_name}: Prioritize micro-irrigation (drip/sprinkler) for cash crops. Avoid midday canal flooding to minimize evaporation loss."
        },
        {
            'category': 'Integrated Pest Management (IPM)',
            'alert_type': 'success',
            'message': "Erect pheromone traps and light traps across fields to monitor nocturnal pest flights before committing to any chemical purchase."
        },
        {
            'category': 'Livestock Seasonal Care',
            'alert_type': 'info',
            'message': "Ensure routine vaccination against Foot & Mouth Disease (FMD) and Haemorrhagic Septicaemia (HS) through your local Government Veterinary Dispensary."
        }
    ]
