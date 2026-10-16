def triage_animal(symptoms, animal_type=None, severity_inputs=None):
    """
    Conservative, rule-based triage stub.
    Returns one of: 'emergency', 'urgent', 'routine' and a short explanation and recommended immediate actions.
    This module must be reviewed by a veterinarian before offering clinical guidance.
    """
    # Simple placeholder rules for demo purposes only.
    red_flags = ['difficulty breathing', 'collapse', 'seizure', 'severe bleeding', 'unable to stand']
    text = (symptoms or '').lower()
    for flag in red_flags:
        if flag in text:
            return {'category': 'emergency', 'explanation': f'Found red-flag symptom: {flag}. Seek immediate veterinary care.'}
    if 'not eating' in text or 'not drinking' in text or 'reduced milk' in text:
        return {'category': 'urgent', 'explanation': 'Decreased eating/drinking or milk production — seek veterinary advice soon.'}
    return {'category': 'routine', 'explanation': 'Monitor the animal, provide supportive care, and contact your vet if symptoms worsen.'}
