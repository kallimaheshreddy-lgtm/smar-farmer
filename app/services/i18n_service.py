"""
Localization service supporting English, Telugu (తెలుగు), and Hindi (हिन्दी)
Provides UI translation dictionaries and helper functions.
"""
from flask import session, request

SUPPORTED_LANGUAGES = {
    'en': 'English',
    'te': 'తెలుగు (Telugu)',
    'hi': 'हिन्दी (Hindi)'
}

TRANSLATIONS = {
    'en': {
        'app_name': 'Smart Farmer AI',
        'app_tagline': 'Smart Farming & Animal Health Assistant for Indian Farmers',
        'home': 'Home',
        'dashboard': 'Farmer Dashboard',
        'plant_checker': 'Plant Disease Checker',
        'animal_checker': 'Animal Health Triage',
        'crop_guide': 'Crop Treatments',
        'fertilizer_guide': 'Fertilizer Guide',
        'weather': 'Weather Dashboard',
        'my_farm': 'My Farm',
        'animal_records': 'Animal Records',
        'history': 'History',
        'vet_contacts': 'Veterinary Directory',
        'admin_panel': 'Admin Dashboard',
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        'profile': 'My Profile',
        'language': 'Language',
        'emergency_helpline': 'Emergency Kisan & Vet Helplines',
        'kisan_call_center': 'Kisan Call Centre: 1800-180-1551 (Toll Free)',
        'pashu_call_center': 'National Animal Health Helpline: 1962 (Toll Free)',
        
        # Dashboard & Home
        'welcome': 'Welcome',
        'quick_actions': 'Quick Actions',
        'check_plant': 'Check Plant Health',
        'check_animal': 'Check Animal Health',
        'view_crops': 'Manage My Crops',
        'view_livestock': 'Manage Livestock',
        'active_crops': 'Active Crops',
        'livestock_head': 'Livestock Count',
        'recent_assessments': 'Recent Assessments',
        'recent_triage': 'Recent Animal Triage',
        'todays_weather': "Today's Weather & Advisory",
        
        # Plant Assessment
        'plant_title': 'Plant Disease & Health Checker',
        'plant_subtitle': 'Upload an image of the affected plant or select symptoms for preliminary agronomic screening.',
        'crop_type': 'Crop Type',
        'select_crop': '-- Select Crop --',
        'growth_stage': 'Growth Stage',
        'affected_parts': 'Affected Plant Parts',
        'observed_symptoms': 'Observed Symptoms',
        'symptom_duration': 'Symptom Duration (Days)',
        'upload_image': 'Upload Clear Photo of Affected Leaf / Stem',
        'assess_button': 'Analyze Plant Health',
        'assessment_result': 'Plant Health Assessment',
        'confidence_score': 'Confidence / Match Score',
        'potential_issue': 'Identified Condition / Pest',
        'supporting_reasons': 'Supporting Observations',
        'alternative_causes': 'Alternative Explanations',
        'recommended_steps': 'Recommended Integrated Pest / Disease Management (IPM)',
        'safety_precautions': 'Safety & Environmental Precautions',
        'source_institution': 'Verified Source Reference',
        'review_date': 'Last Verified Date',
        'expert_inspection_note': 'Agronomist Inspection Recommendation',
        'plant_disclaimer': 'Important Notice: This tool provides preliminary screening based on visible symptoms and verified agricultural extension literature (ICAR / State Agricultural Universities). It does not replace field inspection by local Krishi Vigyan Kendra (KVK) officers or certified agronomists. Never apply unverified chemicals or off-label pesticides.',
        
        # Animal Health
        'animal_title': 'Livestock Health Triage & Interim Care',
        'animal_subtitle': 'Conservative triage assistance for cows, buffaloes, goats, sheep, and poultry. Prioritizes urgent veterinary intervention for danger signs.',
        'select_species': 'Livestock Species',
        'animal_age': 'Approximate Age',
        'appetite': 'Appetite / Feeding',
        'behavior': 'Behavior & Energy',
        'temperature': 'Body Temperature Perception',
        'breathing': 'Breathing Pattern',
        'standing': 'Mobility / Standing Ability',
        'milk_yield': 'Milk Yield Drop (if applicable)',
        'other_symptoms': 'Additional Symptoms Observed',
        'triage_button': 'Evaluate Triage Level',
        'triage_result': 'Veterinary Triage Assessment',
        'urgency_level': 'Triage Urgency Level',
        'emergency': 'CRITICAL EMERGENCY — Call Veterinarian Immediately',
        'urgent': 'URGENT — Veterinary Attention Needed within 12-24 Hours',
        'monitor': 'MONITOR & SUPPORTIVE CARE — Conservative Management',
        'immediate_actions': 'Safe Interim Supportive Care',
        'what_not_to_do': 'Strict Restrictions & What NOT to Do',
        'animal_disclaimer': 'STRICT VETERINARY SAFEGUARD: Smart Farmer AI does NOT prescribe antibiotics, prescription injections, or schedule veterinary pharmaceuticals. Diagnosis and prescription must only be performed by a qualified veterinary doctor. If danger signs (severe bloat, recumbency, foaming, high fever, bleeding) are present, contact your nearest veterinary dispensary or dial 1962 immediately without delay.',
        
        # Knowledge Base & Guides
        'search_placeholder': 'Search crops, diseases, pests, fertilizers...',
        'category_filter': 'All Categories',
        'verified_treatments': 'Verified Agricultural Management',
        'fertilizer_schedule': 'Crop Nutrient & Fertilizer Schedules',
        'npk_ratio': 'Recommended N:P:K Ratio (kg/ha)',
        'organic_manures': 'Organic & Bio-fertilizer Integration',
        'application_tips': 'Application Timing & Soil Moisture Rules',
        
        # Common UI
        'view_details': 'View Details',
        'back_to_list': 'Back to List',
        'save': 'Save Record',
        'delete': 'Delete',
        'edit': 'Edit',
        'submit': 'Submit',
        'cancel': 'Cancel',
        'call_now': 'Call Veterinary Center',
        'status': 'Status',
        'date': 'Date',
        'actions': 'Actions',
        'no_records': 'No records found yet.',
        'all_rights_reserved': 'Empowering Indian Farmers with Responsible AI & Verified Agricultural Science.'
    },
    'te': {
        'app_name': 'స్మార్ట్ ఫార్మర్ AI',
        'app_tagline': 'భారతీయ రైతుల కోసం స్మార్ట్ వ్యవసాయ మరియు పశు ఆరోగ్య సహాయకుడు',
        'home': 'హోమ్',
        'dashboard': 'రైతు డ్యాష్‌బోర్డ్',
        'plant_checker': 'మొక్కల వ్యాధి పరీక్ష',
        'animal_checker': 'పశువుల ఆరోగ్య పరీక్ష',
        'crop_guide': 'పంట చికిత్స మార్గదర్శి',
        'fertilizer_guide': 'ఎరువుల మార్గదర్శి',
        'weather': 'వాతావరణ నివేదిక',
        'my_farm': 'నా వ్యవసాయం',
        'animal_records': 'పశువుల రికార్డులు',
        'history': 'పూర్వ రికార్డులు',
        'vet_contacts': 'పశువైద్య డైరెక్టరీ',
        'admin_panel': 'అడ్మిన్ డ్యాష్‌బోర్డ్',
        'login': 'లాగిన్',
        'register': 'రిజిస్టర్',
        'logout': 'లాగౌట్',
        'profile': 'నా ప్రొఫైల్',
        'language': 'భాష',
        'emergency_helpline': 'అత్యవసర కిసాన్ & పశువుల హెల్ప్‌లైన్',
        'kisan_call_center': 'కిసాన్ కాల్ సెంటర్: 1800-180-1551 (ఉచిత కాల్)',
        'pashu_call_center': 'జాతీయ పశు ఆరోగ్య హెల్ప్‌లైన్: 1962 (ఉచిత కాల్)',
        
        # Dashboard & Home
        'welcome': 'స్వాగతం',
        'quick_actions': 'త్వరిత సేవలు',
        'check_plant': 'మొక్క ఆరోగ్యం తనిఖీ చేయండి',
        'check_animal': 'పశువు ఆరోగ్యం తనిఖీ చేయండి',
        'view_crops': 'నా పంటల వివరాలు',
        'view_livestock': 'పశువుల వివరాలు',
        'active_crops': 'ప్రస్తుత పంటలు',
        'livestock_head': 'మొత్తం పశువులు',
        'recent_assessments': 'ఇటీవలి పంట పరీక్షలు',
        'recent_triage': 'ఇటీవలి పశు పరీక్షలు',
        'todays_weather': 'నేటి వాతావరణం & వ్యవసాయ సలహా',
        
        # Plant Assessment
        'plant_title': 'మొక్కల వ్యాధి మరియు ఆరోగ్య పరీక్ష',
        'plant_subtitle': 'లక్షణాలను గుర్తించడానికి మొక్క యొక్క ఫోటోను అప్‌లోడ్ చేయండి లేదా లక్షణాలను ఎంచుకోండి.',
        'crop_type': 'పంట రకం',
        'select_crop': '-- పంటను ఎంచుకోండి --',
        'growth_stage': 'పంట దశ',
        'affected_parts': 'ప్రభావితమైన భాగాలు',
        'observed_symptoms': 'గమనించిన లక్షణాలు',
        'symptom_duration': 'లక్షణాలు ప్రారంభమైన రోజులు',
        'upload_image': 'ఆకు లేదా కాండం యొక్క స్పష్టమైన ఫోటోను ఎంచుకోండి',
        'assess_button': 'మొక్క ఆరోగ్యాన్ని విశ్లేషించండి',
        'assessment_result': 'మొక్క ఆరోగ్య నివేదిక',
        'confidence_score': 'లక్షణాల సరిపోలిక శాతం',
        'potential_issue': 'గుర్తించబడిన సమస్య / తెగులు',
        'supporting_reasons': 'సమర్ధించే కారణాలు',
        'alternative_causes': 'ఇతర సంభావ్య కారణాలు',
        'recommended_steps': 'సిఫార్సు చేయబడిన సమగ్ర సస్యరక్షణ చర్యలు (IPM)',
        'safety_precautions': 'రక్షణ మరియు పర్యావరణ జాగ్రత్తలు',
        'source_institution': 'ధృవీకరించబడిన మూలం',
        'review_date': 'చివరి సమీక్ష తేదీ',
        'expert_inspection_note': 'వ్యవసాయ శాస్త్రవేత్త పరిశీలన సూచన',
        'plant_disclaimer': 'ముఖ్య గమనిక: ఈ అప్లికేషన్ అధికారిక వ్యవసాయ విశ్వవిద్యాలయాల (ICAR / ANGRAU) సమాచారం ఆధారంగా ప్రాథమిక పరిశీలనను మాత్రమే అందిస్తుంది. ఇది స్థానిక కృషి విజ్ఞాన కేంద్రం (KVK) అధికారుల ప్రత్యక్ష తనిఖీకి ప్రత్యామ్నాయం కాదు.',
        
        # Animal Health
        'animal_title': 'పశువుల ఆరోగ్య పరీక్ష మరియు ప్రథమ చికిత్స',
        'animal_subtitle': 'ఆవులు, గేదెలు, మేకలు, గొర్రెలు, కోళ్ళ కొరకు సురక్షితమైన ఆరోగ్య అంచనా. ప్రమాద సంకేతాలు ఉన్నప్పుడు వెంటనే పశువైద్యుడిని సంప్రదించండి.',
        'select_species': 'పశువు రకం',
        'animal_age': 'సుమారు వయస్సు',
        'appetite': 'మేత / నీరు తీసుకోవడం',
        'behavior': 'ప్రవర్తన & చురుకుదనం',
        'temperature': 'శరీర ఉష్ణోగ్రత స్థితి',
        'breathing': 'శ్వాస తీసుకోవడం',
        'standing': 'నిలబడే సామర్థ్యం / కదలిక',
        'milk_yield': 'పాల దిగుబడి తగ్గుదల (అవసరమైతే)',
        'other_symptoms': 'ఇతర గమనించిన లక్షణాలు',
        'triage_button': 'పరిస్థితిని అంచనా వేయండి',
        'triage_result': 'పశు ఆరోగ్య నివేదిక',
        'urgency_level': 'పరిస్థితి తీవ్రత',
        'emergency': 'అత్యవసర పరిస్థితి — వెంటనే పశువైద్యుడిని పిలవండి',
        'urgent': 'ముఖ్యమైనది — 12-24 గంటల్లో పశువైద్యుడి వద్దకు తీసుకెళ్లండి',
        'monitor': 'సాధారణ పర్యవేక్షణ — ప్రథమ సంరక్షణ చర్యలు',
        'immediate_actions': 'తక్షణ సంరక్షణ సూచనలు',
        'what_not_to_do': 'చేయకూడని పనులు & కఠిన ఆంక్షలు',
        'animal_disclaimer': 'కఠిన పశువైద్య నిబంధన: స్మార్ట్ ఫార్మర్ AI ఎలాంటి యాంటీబయోటిక్స్ లేదా ఇంజెక్షన్లను నేరుగా సూచించదు. ప్రిస్క్రిప్షన్ కేవలం అర్హత కలిగిన పశువైద్యుల ద్వారా మాత్రమే జరగాలి. తీవ్రమైన లక్షణాలు ఉంటే వెంటనే 1962 కి కాల్ చేయండి.',
        
        # Knowledge Base & Guides
        'search_placeholder': 'పంటలు, తెగుళ్ళు, ఎరువులు లేదా వ్యాధుల కోసం వెతకండి...',
        'category_filter': 'అన్ని విభాగాలు',
        'verified_treatments': 'ధృవీకరించబడిన వ్యవసాయ నివారణలు',
        'fertilizer_schedule': 'పంట ఎరువుల ప్రణాళిక',
        'npk_ratio': 'సిఫార్సు చేసిన N:P:K నిష్పత్తి (కేజీ/హెక్టారుకు)',
        'organic_manures': 'సేంద్రీయ ఎరువుల వినియోగం',
        'application_tips': 'ఎరువులు వేసే సరైన సమయం & నేల తేమ నిబంధనలు',
        
        # Common UI
        'view_details': 'వివరాలు చూడండి',
        'back_to_list': 'జాబితాకు తిరిగి వెళ్లండి',
        'save': 'రికార్డ్ భద్రపరచండి',
        'delete': 'తొలగించండి',
        'edit': 'సవరించండి',
        'submit': 'సమర్పించండి',
        'cancel': 'రద్దు చేయండి',
        'call_now': 'పశువైద్యుడికి కాల్ చేయండి',
        'status': 'స్థితి',
        'date': 'తేదీ',
        'actions': 'చర్యలు',
        'no_records': 'ఇంకా ఎలాంటి రికార్డులు లేవు.',
        'all_rights_reserved': 'బాధ్యతాయుతమైన సాంకేతికతతో భారతీయ రైతులకు అండగా.'
    },
    'hi': {
        'app_name': 'स्मार्ट फार्मर AI',
        'app_tagline': 'भारतीय किसानों के लिए स्मार्ट कृषि और पशु स्वास्थ्य सहायक',
        'home': 'होम',
        'dashboard': 'किसान डैशबोर्ड',
        'plant_checker': 'पौध रोग जांच',
        'animal_checker': 'पशु स्वास्थ्य जांच',
        'crop_guide': 'फसल उपचार निर्देशिका',
        'fertilizer_guide': 'उर्वरक एवं खाद गाइड',
        'weather': 'मौसम डैशबोर्ड',
        'my_farm': 'मेरा खेत',
        'animal_records': 'पशुधन रिकॉर्ड',
        'history': 'इतिहास',
        'vet_contacts': 'पशु चिकित्सक संपर्क',
        'admin_panel': 'व्यवस्थापक डैशबोर्ड',
        'login': 'लॉग इन',
        'register': 'पंजीकरण',
        'logout': 'लॉग आउट',
        'profile': 'मेरी प्रोफाइल',
        'language': 'भाषा',
        'emergency_helpline': 'आपातकालीन किसान एवं पशु हेल्पलाइन',
        'kisan_call_center': 'किसान कॉल सेंटर: 1800-180-1551 (निःशुल्क)',
        'pashu_call_center': 'राष्ट्रीय पशु स्वास्थ्य हेल्पलाइन: 1962 (निःशुल्क)',
        
        # Dashboard & Home
        'welcome': 'स्वागत है',
        'quick_actions': 'त्वरित सेवाएं',
        'check_plant': 'पौधे का स्वास्थ्य जांचें',
        'check_animal': 'पशु स्वास्थ्य का आकलन करें',
        'view_crops': 'मेरी फसलें देखें',
        'view_livestock': 'पशुधन देखें',
        'active_crops': 'वर्तमान फसलें',
        'livestock_head': 'पशुओं की संख्या',
        'recent_assessments': 'हाल की पौध जांच',
        'recent_triage': 'हाल की पशु जांच',
        'todays_weather': 'आज का मौसम और कृषि सलाह',
        
        # Plant Assessment
        'plant_title': 'पौध रोग एवं स्वास्थ्य परीक्षण',
        'plant_subtitle': 'लक्षणों की पहचान के लिए प्रभावित पौधे की फोटो अपलोड करें या लक्षण चुनें।',
        'crop_type': 'फसल का प्रकार',
        'select_crop': '-- फसल चुनें --',
        'growth_stage': 'फसल की अवस्था',
        'affected_parts': 'प्रभावित भाग',
        'observed_symptoms': 'देखे गए लक्षण',
        'symptom_duration': 'लक्षणों की अवधि (दिन)',
        'upload_image': 'पत्ती या तने की स्पष्ट फोटो चुनें',
        'assess_button': 'पौध स्वास्थ्य का विश्लेषण करें',
        'assessment_result': 'पौध स्वास्थ्य रिपोर्ट',
        'confidence_score': 'लक्षण मिलान प्रतिशत',
        'potential_issue': 'पहचानी गई समस्या / रोग',
        'supporting_reasons': 'समर्थक कारण',
        'alternative_causes': 'अन्य संभावित कारण',
        'recommended_steps': 'सिफारिश किए गए एकीकृत कीट/रोग प्रबंधन (IPM)',
        'safety_precautions': 'सुरक्षा एवं पर्यावरण सावधानियां',
        'source_institution': 'सत्यापित स्रोत संदर्भ',
        'review_date': 'अंतिम समीक्षा तिथि',
        'expert_inspection_note': 'कृषि वैज्ञानिक द्वारा निरीक्षण की अनुशंसा',
        'plant_disclaimer': 'महत्वपूर्ण सूचना: यह उपकरण प्रमाणित कृषि विश्वविद्यालयों (ICAR / राज्य कृषि विश्वविद्यालय) के साहित्य पर आधारित प्रारंभिक परीक्षण प्रदान करता है। यह कृषि विज्ञान केंद्र (KVK) के विशेषज्ञों द्वारा प्रत्यक्ष निरीक्षण का विकल्प नहीं है। कभी भी गैर-प्रमाणित रसायनों का छिड़काव न करें।',
        
        # Animal Health
        'animal_title': 'पशु स्वास्थ्य ट्रायज एवं प्राथमिक देखभाल',
        'animal_subtitle': 'गाय, भैंस, बकरी, भेड़ और मुर्गियों के लिए रूढ़िवादी स्वास्थ्य मूल्यांकन। खतरे के संकेत मिलने पर तुरंत पशु चिकित्सक से संपर्क करें।',
        'select_species': 'पशु की प्रजाति',
        'animal_age': 'अनुमानित आयु',
        'appetite': 'चारा / पानी की स्थिति',
        'behavior': 'व्यवहार और सुस्ती',
        'temperature': 'शारीरिक तापमान की स्थिति',
        'breathing': 'सांस लेने की स्थिति',
        'standing': 'खड़े होने की क्षमता / गतिशीलता',
        'milk_yield': 'दूध उत्पादन में कमी (यदि लागू हो)',
        'other_symptoms': 'अन्य देखे गए लक्षण',
        'triage_button': 'स्थिति का आकलन करें',
        'triage_result': 'पशु स्वास्थ्य आकलन परिणाम',
        'urgency_level': 'गंभीरता का स्तर',
        'emergency': 'अत्यंत गंभीर आपातकाल — तुरंत पशु चिकित्सक को बुलाएं',
        'urgent': 'आवश्यक — 12-24 घंटे के भीतर पशु चिकित्सक को दिखाएं',
        'monitor': 'सामान्य निगरानी — प्राथमिक देखभाल एवं अवलोकन',
        'immediate_actions': 'सुरक्षित प्राथमिक देखभाल निर्देश',
        'what_not_to_do': 'सख्त प्रतिबंध एवं क्या न करें',
        'animal_disclaimer': 'सख्त पशु चिकित्सा सुरक्षा नियम: स्मार्ट फार्मर AI किसी भी एंटीबायोटिक या इंजेक्शन की दवा नहीं लिखता है। दवा केवल पंजीकृत पशु चिकित्सक द्वारा ही दी जानी चाहिए। खतरे के संकेत होने पर बिना देर किए तुरंत 1962 पर कॉल करें।',
        
        # Knowledge Base & Guides
        'search_placeholder': 'फसलें, रोग, कीट, खाद या पशु स्वास्थ्य खोजें...',
        'category_filter': 'सभी श्रेणियां',
        'verified_treatments': 'प्रमाणित कृषि उपचार',
        'fertilizer_schedule': 'फसल पोषण एवं उर्वरक सारणी',
        'npk_ratio': 'अनुशंसित N:P:K अनुपात (किग्रा/हेक्टेयर)',
        'organic_manures': 'जैविक खाद एवं जैव-उर्वरक',
        'application_tips': 'उर्वरक देने का सही समय एवं नमी नियम',
        
        # Common UI
        'view_details': 'विवरण देखें',
        'back_to_list': 'सूची पर वापस जाएं',
        'save': 'रिकॉर्ड सुरक्षित करें',
        'delete': 'हटाएं',
        'edit': 'संपादित करें',
        'submit': 'जमा करें',
        'cancel': 'रद्द करें',
        'call_now': 'पशु चिकित्सालय को कॉल करें',
        'status': 'स्थिति',
        'date': 'तिथि',
        'actions': 'कार्य',
        'no_records': 'कोई रिकॉर्ड नहीं मिला।',
        'all_rights_reserved': 'जिम्मेदार तकनीक से भारतीय किसानों को सशक्त बनाना।'
    }
}


def get_current_locale():
    """Retrieve active language from session, user preference, or query param, defaulting to 'en'."""
    lang = request.args.get('lang')
    if lang in SUPPORTED_LANGUAGES:
        session['locale'] = lang
        return lang
    if 'locale' in session and session['locale'] in SUPPORTED_LANGUAGES:
        return session['locale']
    return 'en'


def t(key, default=None):
    """Translate key for currently active locale."""
    locale = get_current_locale()
    locale_dict = TRANSLATIONS.get(locale, TRANSLATIONS['en'])
    val = locale_dict.get(key)
    if val is not None:
        return val
    return TRANSLATIONS['en'].get(key, default or key)
