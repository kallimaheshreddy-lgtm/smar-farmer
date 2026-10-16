import os

MODEL_API_URL = os.environ.get('MODEL_API_URL')


def assess_plant(images, crop_type=None, variety=None, growth_stage=None, symptoms_text=None):
    """
    Stubbed plant assessment service.
    If MODEL_API_URL is configured, this should call the external model API and return structured results.
    Otherwise return None to indicate no model available and let the UI show the safe manual workflow.
    """
    if not MODEL_API_URL:
        return None

    # Example API contract (to be implemented when a real model endpoint is available):
    # POST { images: [multipart files], meta: {crop_type, variety, growth_stage, symptoms_text} }
    # Response: {predictions: [{label: '...', confidence: 0.92}, ...], notes: '...' }

    # For now, do not attempt network calls here; keep behavior deterministic for demos.
    return None
