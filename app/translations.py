from app.services.i18n_service import TRANSLATIONS, t, get_current_locale, SUPPORTED_LANGUAGES

def get_text(key, lang='en'):
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS.get('en', {}))
    val = lang_dict.get(key)
    if val is not None:
        return val
    return TRANSLATIONS.get('en', {}).get(key, key)
