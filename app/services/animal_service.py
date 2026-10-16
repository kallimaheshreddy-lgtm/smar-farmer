"""
Animal Health Triage Service.
Conservative veterinary triage workflow for Indian livestock:
Cows, Buffaloes, Goats, Sheep, Poultry, and other domestic animals.
Strictly adheres to veterinary ethics: No drug prescriptions or clinical diagnosis.
Prioritizes emergency red flags and safe interim nursing care.
"""
import os
from PIL import Image

# Red-flag clinical emergency signs that mandate immediate veterinary care
EMERGENCY_DANGER_SIGNS = [
    'unable to stand', 'downer', 'collapse', 'cannot stand', 'recumbent',
    'severe bloat', 'tympany', 'distended stomach', 'swollen left flank',
    'choking', 'gasping for breath', 'severe breathing difficulty', 'open mouth breathing',
    'bleeding from nose', 'bleeding from rectum', 'blood in urine', 'red urine',
    'convulsions', 'seizures', 'head pressing', 'circling', 'shivering violently',
    'foaming at mouth', 'frothing', 'profuse salivation',
    'cold udder with blue or black discolouration', 'gangrenous mastitis',
    'sudden death of multiple birds', 'high flock mortality',
    'prolapse of uterus', 'rectal prolapse',
    'straining for hours during delivery', 'dystocia', 'calving difficulty'
]

# Urgent warning signs requiring a vet visit within 12 to 24 hours
URGENT_WARNING_SIGNS = [
    'high fever', 'burning hot horns', 'very hot body',
    'completely stopped eating', 'off feed for 24 hours', 'not eating',
    'swollen painful udder', 'blood in milk', 'clots in milk', 'mastitis',
    'severe diarrhea with foul smell', 'black watery dung',
    'drooling with mouth blisters', 'blisters on hooves', 'foot and mouth',
    'rapid shallow breathing', 'continuous deep coughing',
    'severe lameness', 'hoof rot', 'maggot wound',
    'cloudy or white eye with blindness', 'severe dehydration with sunken eyes'
]


def analyze_animal_image_features(image_path):
    """
    Performs visual inspection of animal symptom image using Pillow:
    Detects severe redness/inflammation (erythema), purulent discharge (pale yellow/white),
    and necrotic/ulcerative tissue (dark tissue).
    """
    if not image_path or not os.path.exists(image_path):
        return None

    try:
        with Image.open(image_path) as img:
            rgb_img = img.convert('RGB')
            sample = rgb_img.resize((150, 150))
            pixels = list(sample.getdata())
            total = len(pixels)
            if total == 0:
                return None

            red_inflamed_count = 0
            dark_ulcer_count = 0
            pale_discharge_count = 0

            for r, g, b in pixels:
                # Acute inflammation / open wound: High Red, low Green & Blue
                if r > 135 and g < 95 and b < 85:
                    red_inflamed_count += 1
                # Dark necrotic / gangrenous tissue
                elif r < 45 and g < 45 and b < 45:
                    dark_ulcer_count += 1
                # Purulent discharge / cloudy opacity
                elif r > 175 and g > 170 and b > 135 and abs(r - g) < 25:
                    pale_discharge_count += 1

            return {
                'inflammation_pct': round(red_inflamed_count / total, 3),
                'ulcer_pct': round(dark_ulcer_count / total, 3),
                'discharge_pct': round(pale_discharge_count / total, 3),
                'total_pixels': total
            }
    except Exception:
        return None


def evaluate_animal_triage(
    species='Cow',
    age_approx=None,
    symptoms_selected=None,
    symptoms_notes=None,
    appetite='normal',
    behavior='alert',
    temperature_status='normal',
    breathing_status='normal',
    standing_status='normal',
    milk_yield_drop='none',
    image_filename=None
):
    """
    Performs conservative veterinary triage assessment.
    Returns urgency level ('emergency', 'urgent', 'monitor'), detailed reasoning,
    safe interim nursing care steps, strict prohibitions, and emergency contact flags.
    """
    species_name = (species or 'Livestock').strip()
    symptoms_text = f"{symptoms_selected or ''} {symptoms_notes or ''}".lower()
    
    # 1. Check for Critical Emergency Flags
    emergency_reasons = []
    
    # Check standing ability
    if standing_status in ['unable', 'downer', 'cannot_stand']:
        emergency_reasons.append("Animal is recumbent / unable to stand (Downer condition). High risk of irreversible muscle and nerve damage.")
        
    # Check breathing
    if breathing_status in ['distress', 'gasping', 'choking']:
        emergency_reasons.append("Severe respiratory distress or gasping detected.")
        
    # Check keyword dangers
    for sign in EMERGENCY_DANGER_SIGNS:
        if sign in symptoms_text:
            emergency_reasons.append(f"Critical clinical warning sign identified: '{sign.title()}'.")
            
    if emergency_reasons:
        return {
            'urgency_level': 'emergency',
            'urgency_title': 'CRITICAL EMERGENCY — Immediate Veterinary Attention Required',
            'badge_color': 'danger',
            'requires_immediate_vet': True,
            'reasons': emergency_reasons,
            'interim_guidance': (
                "1. CALL A VETERINARIAN OR DIAL THE 1962 TOLL-FREE ANIMAL HELPLINE IMMEDIATELY.\n"
                "2. Provide calm, quiet, draft-free shelter with soft bedding (straw or dry sand).\n"
                "3. If severe bloat/tympany: Keep animal in a sternal sitting position with front feet raised; do NOT allow animal to roll on its back.\n"
                "4. If recumbent/unable to stand: Turn animal from side to side every 2 hours to prevent lung congestion and pressure sores.\n"
                "5. Isolate from rest of the herd to prevent panic or trampling."
            ),
            'what_not_to_do': (
                "• DO NOT DRENCH or force-feed any oils, water, or home remedies by mouth. If animal is choking or recumbent, liquid will enter lungs causing fatal aspiration pneumonia!\n"
                "• DO NOT administer prescription injections or antibiotics without a licensed veterinarian's direct examination.\n"
                "• DO NOT brand, cut ears, or use harmful folk practices."
            ),
            'helpline': '1962 (National Animal Helpline - 24x7 Free)'
        }
        
    # 2. Check for Urgent Veterinary Signs (12-24 hours)
    urgent_reasons = []
    
    # Check visual image features if animal photo is provided
    visual_features = None
    if image_filename:
        img_path = image_filename
        if not os.path.isabs(img_path):
            try:
                from flask import current_app
                upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
                img_path = os.path.join(upload_folder, image_filename)
            except Exception:
                img_path = image_filename
        if os.path.exists(img_path):
            visual_features = analyze_animal_image_features(img_path)

    if visual_features:
        if visual_features['inflammation_pct'] >= 0.04:
            urgent_reasons.append(f"Visual photo analysis detected active cutaneous inflammation/erythema ({int(visual_features['inflammation_pct']*100)}% red lesion index).")
        if visual_features['ulcer_pct'] >= 0.05:
            urgent_reasons.append(f"Visual photo analysis detected localized ulcerative or necrotic tissue ({int(visual_features['ulcer_pct']*100)}% ulcer index).")
        if visual_features['discharge_pct'] >= 0.08:
            urgent_reasons.append(f"Visual photo analysis detected purulent exudate / discharge ({int(visual_features['discharge_pct']*100)}% discharge index).")
    
    if appetite in ['stopped', 'off_feed']:
        urgent_reasons.append("Animal has completely stopped taking feed or water.")
    if behavior in ['dull', 'lethargic', 'depressed']:
        urgent_reasons.append("Animal appears markedly dull, depressed, or lethargic.")
    if temperature_status in ['high_fever', 'cold']:
        urgent_reasons.append("Abnormal body temperature (suspected high fever or subnormal temperature).")
    if milk_yield_drop in ['severe', 'acute']:
        urgent_reasons.append("Sudden, acute collapse in milk yield indicating systemic infection or acute mastitis.")
        
    for sign in URGENT_WARNING_SIGNS:
        if sign in symptoms_text:
            urgent_reasons.append(f"Veterinary warning indicator noted: '{sign.title()}'.")
            
    if urgent_reasons:
        return {
            'urgency_level': 'urgent',
            'urgency_title': 'URGENT — Veterinary Examination Recommended within 12–24 Hours',
            'badge_color': 'warning',
            'requires_immediate_vet': False,
            'reasons': urgent_reasons,
            'interim_guidance': (
                "1. Contact your local Veterinary Dispensary or Livestock Assistant for an on-site visit today.\n"
                "2. Isolate the sick animal into a clean, dry, shaded quarantine shed.\n"
                "3. Offer fresh, clean drinking water at room temperature. Provide easily digestible green fodder or rice gruel.\n"
                "4. For mastitis symptoms: Milk out the affected quarter completely into a separate container every 2-3 hours and safely discard. Do NOT mix with herd milk.\n"
                "5. Record body temperature, dung consistency, and feed intake to report to the doctor upon arrival."
            ),
            'what_not_to_do': (
                "• DO NOT administer human painkillers (such as paracetamol or diclofenac) or leftover antibiotics. Certain human drugs cause fatal kidney failure in ruminants.\n"
                "• DO NOT tie the animal tightly in direct harsh sunlight or cold drafts.\n"
                "• DO NOT allow calves or kids to nurse from an inflamed or mastitic teat."
            ),
            'helpline': '1962 (National Animal Helpline - 24x7 Free)'
        }
        
    # 3. Monitor & Conservative Supportive Care
    return {
        'urgency_level': 'monitor',
        'urgency_title': 'MONITOR & SAFE CARE — Non-Emergency Observation',
        'badge_color': 'success',
        'requires_immediate_vet': False,
        'reasons': [
            "No acute danger flags or severe clinical distress detected from current observations.",
            f"Observation logged for {species_name} with mild symptoms."
        ],
        'interim_guidance': (
            "1. Keep animal under close observation for the next 24 to 48 hours.\n"
            "2. Ensure continuous access to clean, fresh drinking water and good quality forage.\n"
            "3. Maintain dry shed hygiene and clean bedding.\n"
            "4. For minor external scratches: Clean gently with mild saline or clean boiled water; apply neem leaf extract or veterinary antiseptic spray.\n"
            "5. If appetite drops, fever develops, or behavior turns sluggish, contact your veterinarian promptly."
        ),
        'what_not_to_do': (
            "• DO NOT neglect monitoring — animals can worsen quickly.\n"
            "• DO NOT introduce sudden dramatic changes in concentrated feed.\n"
            "• DO NOT administer scheduled veterinary drugs without medical oversight."
        ),
        'helpline': '1962 (National Animal Helpline - 24x7 Free)'
    }
