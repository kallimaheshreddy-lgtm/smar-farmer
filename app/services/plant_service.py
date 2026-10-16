"""
Plant Health Assessment Service.
Provides a modular integration interface for genuine deep learning / computer vision models,
with transparent configuration status and verified agronomic fallback rules.
Sources: ICAR institutes, TNAU, ANGRAU, and Central Insecticide Board & Registration Committee (CIBRC) guidance.
"""
import os
import requests
from werkzeug.utils import secure_filename
from PIL import Image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 8 * 1024 * 1024  # 8 MB


def validate_image_file(file_storage):
    """
    Validates uploaded file for extension, MIME-type, and genuine image content via Pillow.
    Returns (is_valid, error_message, sanitized_filename)
    """
    if not file_storage or not file_storage.filename:
        return False, "No file was selected for upload.", None
    
    filename = secure_filename(file_storage.filename)
    if '.' not in filename:
        return False, "File must have an image extension (.jpg, .jpeg, .png, .webp).", None
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"File format '.{ext}' is not supported. Use JPG, PNG, or WEBP.", None
    
    # Verify image integrity via Pillow
    try:
        file_storage.seek(0)
        img = Image.open(file_storage.stream)
        img.verify()
        file_storage.seek(0)
    except Exception:
        return False, "The uploaded file is not a valid or readable image.", None
    
    return True, None, filename


class PlantDiseaseModelInterface:
    """Abstract interface for plant disease classification model integrations."""
    def predict(self, image_path, crop_type=None, symptoms=None):
        raise NotImplementedError("Subclasses must implement predict()")


class RemoteModelAdapter(PlantDiseaseModelInterface):
    """
    Adapter for genuine remote deep learning inference API (e.g., PyTorch/TensorFlow serving endpoint).
    Transparently informs user if credentials/weights are missing.
    """
    def __init__(self, endpoint_url=None, api_key=None):
        self.endpoint_url = endpoint_url or os.environ.get('MODEL_API_URL')
        self.api_key = api_key or os.environ.get('MODEL_API_KEY')

    def is_configured(self):
        return bool(self.endpoint_url and self.endpoint_url.strip())

    def predict(self, image_path, crop_type=None, symptoms=None):
        if not self.is_configured():
            return None, "Model endpoint (MODEL_API_URL) is not configured in application environment."
        
        try:
            with open(image_path, 'rb') as f:
                files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
                data = {'crop_type': crop_type or '', 'symptoms': symptoms or ''}
                headers = {}
                if self.api_key:
                    headers['Authorization'] = f"Bearer {self.api_key}"
                
                resp = requests.post(self.endpoint_url, files=files, data=data, headers=headers, timeout=10)
                if resp.status_code == 200:
                    payload = resp.json()
                    return payload, None
                else:
                    return None, f"Model service returned status {resp.status_code}: {resp.text[:120]}"
        except Exception as e:
            return None, f"Could not connect to model inference endpoint: {str(e)}"


# Verified Knowledge Repository for Agronomic Assessment
VERIFIED_CROP_CONDITIONS = {
    'Rice': [
        {
            'name': 'Rice Blast (Pyricularia oryzae)',
            'match_keywords': ['spindle', 'boat', 'leaf spot', 'eye shaped', 'lesion', 'drying', 'brown spot with grey centre', 'neck blast'],
            'supporting_reasons': 'Spindle or eye-shaped lesions with grey centers and brown borders on leaves or panicle nodes. Favored by high humidity and excessive nitrogen.',
            'alternatives': 'Brown spot (Bipolaris oryzae), Sheath blight, or potassium deficiency.',
            'recommended_steps': '1. Balanced fertilizer application: Avoid excessive nitrogenous fertilizers.\n2. Water management: Maintain shallow water layer.\n3. Biological control: Foliar spray of Pseudomonas fluorescens @ 2.5 kg/ha or Trichoderma harzianum.\n4. Field hygiene: Burn or bury infected stubble after harvest.',
            'safety_precautions': 'Always wear protective face mask and gloves during foliar sprays. Maintain a safe waiting period (PHI) before harvest. Never discharge spray equipment washings into ponds or drinking water sources.',
            'source': 'ICAR - Indian Institute of Rice Research (IIRR), Hyderabad & TNAU Agritech Portal',
            'review_date': 'August 2026',
            'requires_expert': True
        },
        {
            'name': 'Bacterial Leaf Blight (Xanthomonas oryzae pv. oryzae)',
            'match_keywords': ['yellowing', 'wavy margin', 'bacterial', 'milky drop', 'wilting', 'water soaked', 'translucent'],
            'supporting_reasons': 'Water-soaked translucent lesions starting from leaf tips and margins, later turning yellow to straw-colored with wavy margins. Bacterial ooze beads may appear on young lesions.',
            'alternatives': 'Zinc deficiency (Khaira disease), iron chlorosis, or salinity injury.',
            'recommended_steps': '1. Drain excess standing field water for 2-3 days.\n2. Delay top-dressing of nitrogen during active disease outbreak.\n3. Grow resistant or tolerant varieties (e.g., Improved Samba Mahsuri - RP Bio-226).\n4. Apply neem oil formulation (3%) or fresh cow dung extract supernatant as traditional bio-spray.',
            'safety_precautions': 'Sterilize pruning tools and avoid moving through wet crop canopies to prevent mechanical spread of bacteria.',
            'source': 'ICAR - National Rice Research Institute (NRRI), Cuttack',
            'review_date': 'July 2026',
            'requires_expert': True
        }
    ],
    'Tomato': [
        {
            'name': 'Early Blight (Alternaria solani)',
            'match_keywords': ['concentric', 'target board', 'brown rings', 'lower leaves', 'blight', 'yellowing halo'],
            'supporting_reasons': 'Concentric dark brown rings resembling a target board, predominantly initiating on older lower foliage with chlorotic yellow halos.',
            'alternatives': 'Septoria leaf spot, Late blight, or physiological leaf roll.',
            'recommended_steps': '1. Remove and destroy affected lower foliage to increase air circulation.\n2. Avoid overhead sprinkler irrigation; prefer drip irrigation to keep foliage dry.\n3. Bio-fungicide: Soil application and foliar spray of Trichoderma viride @ 5g/liter.\n4. 2-year crop rotation with non-solanaceous crops (avoid potato, brinjal, chilli).',
            'safety_precautions': 'Wash hands and tools thoroughly after handling blighted foliage. Avoid working in the field while plants are wet with morning dew.',
            'source': 'ICAR - Indian Institute of Horticultural Research (IIHR), Bengaluru',
            'review_date': 'September 2026',
            'requires_expert': False
        },
        {
            'name': 'Tomato Leaf Curl Virus (ToLCV)',
            'match_keywords': ['curling', 'crinkling', 'upward curling', 'stunted', 'whitefly', 'puckered', 'small leaves'],
            'supporting_reasons': 'Upward and inward curling of leaf margins, thick puckered foliage, interveinal chlorosis, and severe stunting of apical growth.',
            'alternatives': 'Herbicide drift injury, severe mite infestation, or aphid damage.',
            'recommended_steps': '1. Vector Management: Install yellow sticky traps (15-20 traps/acre) to monitor and catch whiteflies (Bemisia tabaci).\n2. Barrier crops: Plant 2-3 border rows of maize, sorghum, or pearl millet 20 days prior to transplanting.\n3. Rogue out and destroy early virus-infected plants within the first 30 days.\n4. Apply 5% Neem Seed Kernel Extract (NSKE) or Neem oil (10,000 ppm @ 2 ml/L) to deter vectors.',
            'safety_precautions': 'Do not burn plastic mulching materials. Safely dispose of vector sticky cards away from livestock.',
            'source': 'Dr. YSR Horticultural University (APHU) & TNAU Plant Pathology',
            'review_date': 'June 2026',
            'requires_expert': True
        }
    ],
    'Cotton': [
        {
            'name': 'Cotton Leaf Curl Virus (CLCuV)',
            'match_keywords': ['curling', 'thickened veins', 'enation', 'leaf curl', 'whitefly', 'upward cup'],
            'supporting_reasons': 'Small vein thickening on underside of leaves, upward cupping of leaves, and formation of cup-shaped leafy enations. Transmitted by whitefly.',
            'alternatives': 'Thrips injury, 2,4-D hormone drift, or sucking pest toxicity.',
            'recommended_steps': '1. Eradicate alternative weed hosts like Kanghi (Abutilon indicum) and Peeli Buti around field bunds.\n2. Install yellow sticky traps (10-12/acre) for whitefly monitoring.\n3. Spray bio-insecticide: Verticillium lecanii @ 5g/liter or NSKE 5%.\n4. Grow CLCuV-tolerant certified hybrids.',
            'safety_precautions': 'Wear long protective clothing when applying botanical sprays. Ensure sprayer calibration.',
            'source': 'ICAR - Central Institute for Cotton Research (CICR), Nagpur',
            'review_date': 'August 2026',
            'requires_expert': True
        },
        {
            'name': 'Bacterial Blight / Angular Leaf Spot (Xanthomonas citri pv. malvacearum)',
            'match_keywords': ['angular', 'water soaked', 'black arm', 'vein blight', 'boll rot'],
            'supporting_reasons': 'Angular water-soaked spots bounded by leaf veinlets, progressing to black arm on petioles and bolls.',
            'alternatives': 'Alternaria leaf spot, Cercospora spot, or hail injury.',
            'recommended_steps': '1. Acid delinting of cotton seed prior to sowing.\n2. Seed treatment with Pseudomonas fluorescens @ 10g/kg seed.\n3. Early rogueing of infected seedlings displaying cotyledonary lesions.\n4. Destruction of crop residues after final harvest.',
            'safety_precautions': 'Never handle acid-delinting without heavy acid-resistant rubber apron, goggles, and gloves.',
            'source': 'ANGRAU Regional Agricultural Research Station, Lam, Guntur',
            'review_date': 'July 2026',
            'requires_expert': True
        }
    ],
    'Chilli': [
        {
            'name': 'Anthracnose & Dieback (Colletotrichum capsici)',
            'match_keywords': ['circular dark spot', 'dieback', 'drying from tip', 'sunken spot', 'black dots on fruit'],
            'supporting_reasons': 'Tips of branches dry downwards (dieback), circular sunken spots on mature fruits with concentric rings of black acervuli.',
            'alternatives': 'Sunscald on fruits, blossom end rot, or Fusarium wilt.',
            'recommended_steps': '1. Collect and burn dried twigs and infected mummified fruits from previous seasons.\n2. Seed treatment with Trichoderma viride @ 4g/kg seed.\n3. Spray Pseudomonas fluorescens @ 5g/L during flowering and fruit setting.\n4. Avoid seed collection from infected fruit lots.',
            'safety_precautions': 'Use dedicated containers for bio-formulations. Avoid direct contact of chilli dust/sap with eyes and mucosal membranes.',
            'source': 'ANGRAU Guntur & ICAR-Indian Institute of Spices Research',
            'review_date': 'August 2026',
            'requires_expert': True
        }
    ],
    'Wheat': [
        {
            'name': 'Yellow / Stripe Rust (Puccinia striiformis)',
            'match_keywords': ['yellow powder', 'stripes', 'pustules', 'rust', 'yellow dust', 'linear rows'],
            'supporting_reasons': 'Bright yellow, powdery pustules arranged in prominent linear stripes along leaf veins. Dust rubs off onto fingers.',
            'alternatives': 'Brown leaf rust, Powdery mildew, or physiological tip necrosis.',
            'recommended_steps': '1. Grow rust-resistant recommended wheat cultivars (e.g., HD-2967, DBW-187, DBW-303).\n2. Regular field scouting during cool, humid spells in Jan-Feb.\n3. Contact local Krishi Vigyan Kendra immediately for early localized patch containment.',
            'safety_precautions': 'Wash work clothes separately after walking through rusted wheat fields to limit spore dissemination.',
            'source': 'ICAR - Indian Institute of Wheat and Barley Research (IIWBR), Karnal',
            'review_date': 'May 2026',
            'requires_expert': True
        }
    ]
}


def perform_agronomic_assessment(crop_type, symptoms_text, growth_stage=None, affected_parts=None, image_filename=None):
    """
    Executes a conservative, evidence-based agronomic screening when deep learning model weights
    are unconfigured or as a second-opinion verification layer.
    """
    crop = (crop_type or '').strip()
    symptoms = (symptoms_text or '').lower()
    
    # Try finding crop category
    conditions = VERIFIED_CROP_CONDITIONS.get(crop)
    if not conditions:
        # Search case-insensitively
        for k, v in VERIFIED_CROP_CONDITIONS.items():
            if k.lower() in crop.lower():
                conditions = v
                break
                
    best_match = None
    best_score = 0
    
    if conditions:
        for cond in conditions:
            score = 0
            for kw in cond['match_keywords']:
                if kw in symptoms:
                    score += 15
            if affected_parts:
                part_lower = affected_parts.lower()
                if 'leaf' in part_lower and 'leaf' in cond['name'].lower():
                    score += 10
                if 'fruit' in part_lower and 'fruit' in cond['name'].lower():
                    score += 10
            if score > best_score:
                best_score = score
                best_match = cond
                
    if best_match and best_score >= 15:
        match_percentage = min(92, 45 + best_score)
        return {
            'detected_issue': best_match['name'],
            'confidence': f"{match_percentage}% (Agronomic Symptom Match)",
            'assessment_mode': 'Verified Agronomic Diagnostic Key',
            'reasons_supporting': best_match['supporting_reasons'],
            'alternative_causes': best_match['alternatives'],
            'recommended_steps': best_match['recommended_steps'],
            'safety_precautions': best_match['safety_precautions'],
            'source_institution': best_match['source'],
            'review_date': best_match['review_date'],
            'requires_expert_visit': best_match['requires_expert'],
            'model_configured': False,
            'model_notice': "Automated Deep Learning Model endpoint is currently unconfigured. Results generated via verified Agricultural University diagnostic keys (ICAR/TNAU/ANGRAU)."
        }
    else:
        # Generic observation
        return {
            'detected_issue': f"Undetermined Foliar / Physiological Issue on {crop or 'Crop'}",
            'confidence': "Preliminary Observation",
            'assessment_mode': 'Agronomic Preliminary Screening',
            'reasons_supporting': f"Symptoms provided: '{symptoms_text or 'Visual abnormality'}'. Observed features do not cleanly match a single pathognomonic disease key without laboratory microscopic examination.",
            'alternative_causes': "Possible micronutrient deficiency (Zinc, Iron, Boron), soil moisture stress, viral infection, or insect vector damage.",
            'recommended_steps': "1. Collect fresh representative leaf specimens in a clean paper envelope.\n2. Do NOT apply broad-spectrum chemical fungicides or pesticides indiscriminately.\n3. Take samples to your nearest Krishi Vigyan Kendra (KVK) or Block Agriculture Office for diagnostic confirmation.\n4. Ensure proper drainage and avoid water stagnation around roots.",
            'safety_precautions': "Do not apply chemical pesticides without confirmed diagnosis and recommendation from an agricultural extension officer. Always consult CIB&RC approved labels.",
            'source_institution': 'ICAR Agricultural Extension Division / State Agricultural Universities',
            'review_date': 'September 2026',
            'requires_expert_visit': True,
            'model_configured': False,
            'model_notice': "Automated Deep Learning Model endpoint is currently unconfigured. Manual assessment applied."
        }
