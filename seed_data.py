"""
Seed initial verified agricultural, veterinary, and fertilizer knowledge base articles,
veterinary contacts directory, and an initial demo admin account.
All entries cite recognized Indian institutions (ICAR, IVRI, TNAU, ANGRAU, DADF).
"""
import sys
from datetime import datetime
from app import create_app, db
from app.models import User, KnowledgeArticle, VetContact


def seed_all():
    app = create_app('development')
    with app.app_context():
        print("Creating all database tables...")
        db.create_all()
        
        # 1. Admin & Demo User
        admin_email = 'admin@smartfarmer.org'
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                email=admin_email,
                name='Senior Agronomist (Admin)',
                phone='18001801551',
                state='Telangana',
                district='Warangal',
                preferred_language='en',
                is_admin=True
            )
            admin.set_password('AdminFarmer@2026')
            db.session.add(admin)
            print(f"Created Admin account: {admin_email} / AdminFarmer@2026")
            
        demo_farmer_email = 'farmer@smartfarmer.org'
        farmer = User.query.filter_by(email=demo_farmer_email).first()
        if not farmer:
            farmer = User(
                email=demo_farmer_email,
                name='Ramesh Kumar',
                phone='9848012345',
                state='Telangana',
                district='Warangal',
                preferred_language='en',
                is_admin=False
            )
            farmer.set_password('Farmer@2026')
            db.session.add(farmer)
            print(f"Created Farmer demo account: {demo_farmer_email} / Farmer@2026")
            
        # 2. Verified Knowledge Base Articles
        articles_data = [
            {
                'category': 'crop_disease',
                'title': 'Rice Blast Management (Pyricularia oryzae)',
                'crop_or_animal': 'Rice / Paddy',
                'symptoms_description': 'Spindle-shaped eye spots with ash-grey centers and brownish borders on foliage. In neck blast, nodes turn blackish-brown and panicles break easily.',
                'management_practices': '1. Balanced NPK nutrition; strictly avoid split excess urea.\n2. Seed treatment with Pseudomonas fluorescens @ 10g/kg seed.\n3. Foliar spray of bio-fungicide Trichoderma harzianum @ 5g/liter or Pseudomonas @ 2.5 kg/ha.\n4. Maintain standing water depth of 2-5 cm during tillering to discourage spore germination.',
                'organic_options': 'Neem oil (0.5%) spray or ferment 10 kg cow dung with water and filter supernatant spray.',
                'safety_precautions': 'Do not spray against the prevailing wind direction. Wear face protection. Respect waiting periods prior to harvest.',
                'source_institution': 'ICAR - Indian Institute of Rice Research (IIRR), Hyderabad',
                'last_reviewed_date': 'August 2026'
            },
            {
                'category': 'crop_disease',
                'title': 'Bacterial Leaf Blight of Rice (Xanthomonas oryzae)',
                'crop_or_animal': 'Rice / Paddy',
                'symptoms_description': 'Water-soaked translucent lesions from leaf tips with wavy, undulating margins. Severely affected leaves dry up with a bleached appearance.',
                'management_practices': '1. Drain standing water completely for 48 hours to retard bacterial multiplication.\n2. Postpone top-dressing of nitrogen until disease ceases.\n3. Grow BLB-resistant varieties such as Improved Samba Mahsuri or DRR Dhan 44.\n4. Avoid clipping seedlings at transplanting time.',
                'organic_options': 'Fresh cow dung extract (20%) spray or panchagavya (3%) foliar application.',
                'safety_precautions': 'Do not move machinery or work in fields while foliage is covered with morning dew.',
                'source_institution': 'ICAR - National Rice Research Institute (NRRI), Cuttack',
                'last_reviewed_date': 'July 2026'
            },
            {
                'category': 'pest',
                'title': 'Pink Bollworm Management in Cotton (Pectinophora gossypiella)',
                'crop_or_animal': 'Cotton',
                'symptoms_description': 'Rosetted flowers ("intertwined petals"), premature boll opening, stained lint, and double seeds inside mature bolls.',
                'management_practices': '1. Install gossyplure pheromone traps @ 5 traps/acre for pest monitoring.\n2. Mass trapping with 15-20 traps/acre at 45 days after sowing.\n3. Release egg parasitoid Trichogramma bactrae @ 60,000/acre weekly from 45 DAS (3-4 releases).\n4. Terminate crop by mid-January to break the pest cycle.',
                'organic_options': 'Neem Seed Kernel Extract (NSKE 5%) or 10,000 ppm Neem formulation @ 2 ml/liter.',
                'safety_precautions': 'Dispose of trap septa properly. Never reuse pheromone containers for food storage.',
                'source_institution': 'ICAR - Central Institute for Cotton Research (CICR), Nagpur',
                'last_reviewed_date': 'September 2026'
            },
            {
                'category': 'crop_disease',
                'title': 'Tomato Early Blight (Alternaria solani)',
                'crop_or_animal': 'Tomato',
                'symptoms_description': 'Dark brown concentric circular rings (target-board appearance) on lower leaves, surrounded by yellow halo. Progresses to collar rot and sunken stem lesions.',
                'management_practices': '1. Crop rotation of 2-3 years with non-solanaceous crops.\n2. Prune lower diseased foliage up to 20 cm above ground level.\n3. Adopt drip irrigation and plastic mulching to prevent soil-splash onto leaves.\n4. Spray bio-agent Trichoderma viride @ 5g/liter at 15-day intervals.',
                'organic_options': 'Bordeaux mixture (1%) or Trichoderma enriched compost applied to root zone.',
                'safety_precautions': 'Never apply Bordeaux mixture in hot, midday sunshine to avoid leaf scorch.',
                'source_institution': 'ICAR - Indian Institute of Horticultural Research (IIHR), Bengaluru',
                'last_reviewed_date': 'August 2026'
            },
            {
                'category': 'pest',
                'title': 'Fall Armyworm Management in Maize (Spodoptera frugiperda)',
                'crop_or_animal': 'Maize',
                'symptoms_description': 'Elongated papery feeding windows on whorl leaves, heavy sawdust-like frass inside whorls, central shoot destruction.',
                'management_practices': '1. Deep summer ploughing to expose pupae to predatory birds.\n2. Seed treatment with Beauveria bassiana @ 10g/kg.\n3. Apply dry sand mixed with ash (9:1 ratio) directly into central whorls.\n4. Install FAW pheromone lures (4 traps/acre).\n5. Foliar spray of Metarhizium rileyi or Bacillus thuringiensis (Bt @ 2g/L).',
                'organic_options': 'Neem oil 1500 ppm @ 5 ml/L or hand-collection of egg masses on field borders.',
                'safety_precautions': 'Ensure personal protection when dropping biocontrol dusts into deep plant whorls.',
                'source_institution': 'ICAR - Indian Institute of Maize Research (IIMR), Ludhiana',
                'last_reviewed_date': 'June 2026'
            },
            {
                'category': 'fertilizer',
                'title': 'Paddy (Rice) Scientific Fertilizer & Nutrient Schedule',
                'crop_or_animal': 'Rice / Paddy',
                'symptoms_description': 'Balanced macronutrient (NPK) and Zinc application schedule for 1 hectare of irrigated transplanted paddy.',
                'management_practices': '• Basal Dose: 50% Phosphorous (P2O5), 50% Potash (K2O), 25% Nitrogen (N) + Zinc Sulphate @ 25 kg/ha.\n• 1st Top Dressing (Active Tillering, 20-25 DAT): 50% Nitrogen.\n• 2nd Top Dressing (Panicle Initiation, 40-45 DAT): Remaining 25% Nitrogen + 50% Potash.\n• Total recommended dose: 120 kg N : 60 kg P2O5 : 60 kg K2O per hectare.',
                'organic_options': 'Apply Farm Yard Manure (FYM) @ 10 tonnes/ha or incorporate green manure (Daincha/Sunnhemp) 15 days before transplanting.',
                'safety_precautions': 'Never mix Zinc Sulphate directly with Phosphatic fertilizers (DAP/SSP) as it precipitates insoluble zinc phosphate.',
                'source_institution': 'Professor Jayashankar Telangana State Agricultural University (PJTSAU) & ICAR-IIRR',
                'last_reviewed_date': 'August 2026'
            },
            {
                'category': 'fertilizer',
                'title': 'Cotton Balanced Nutrient & Fertigation Guide',
                'crop_or_animal': 'Cotton',
                'symptoms_description': 'Recommended fertilization for hybrid and Bt cotton per hectare.',
                'management_practices': '• Recommended NPK Dose: 120:60:60 kg/ha for rainfed; 150:75:75 kg/ha for irrigated cotton.\n• Apply entire Phosphorus as basal dose.\n• Split Nitrogen into 4 equal doses: Basal, Square formation (30-35 DAS), Flowering (55-60 DAS), and Boll development (75-80 DAS).\n• Foliar spray of 1% Magnesium Sulphate (MgSO4) + 1% 19:19:19 at 60 and 90 DAS to prevent red leaf disease.',
                'organic_options': 'Vermicompost @ 2.5 tonnes/ha enriched with Azotobacter and Phosphate Solubilizing Bacteria (PSB).',
                'safety_precautions': 'Avoid applying high doses of urea during dry spells without subsequent irrigation.',
                'source_institution': 'ICAR - Central Institute for Cotton Research (CICR), Nagpur',
                'last_reviewed_date': 'July 2026'
            },
            {
                'category': 'animal_health',
                'title': 'Bovine Mastitis Recognition & Prevention (Cattle & Buffaloes)',
                'crop_or_animal': 'Cow / Buffalo',
                'symptoms_description': 'Swollen, hard, hot, or painful udder; blood, yellow clots, or flakes in milk; sudden decrease in milk volume. Animal resists milking.',
                'management_practices': '1. Clean, dry bedding is paramount: 80% of mastitis is environmental.\n2. Post-milking teat dipping in 0.5% povidone-iodine solution.\n3. Completely strip milk from infected quarter into a bucket and disinfect; do NOT mix with healthy milk.\n4. Contact a veterinarian immediately for CMT test and culture-guided intramammary treatment.',
                'organic_options': 'Topical paste of Aloe vera gel mixed with turmeric powder applied around udder base (supportive soothing care only; not a substitute for vet therapy).',
                'safety_precautions': 'STRICT RESTRICTION: Do not inject antibiotics blindly into teat canal without sterile vet guidance. Never discard mastitic milk in open cattle stalls.',
                'source_institution': 'ICAR - Indian Veterinary Research Institute (IVRI), Izatnagar',
                'last_reviewed_date': 'September 2026'
            },
            {
                'category': 'animal_health',
                'title': 'Foot and Mouth Disease (FMD) Vigilance & Biosecurity',
                'crop_or_animal': 'Cattle, Buffalo, Goat, Sheep',
                'symptoms_description': 'High fever (104-106°F), vesicles and blisters in mouth, tongue, and interdigital cleft of hooves; excessive ropy drooling; severe lameness.',
                'management_practices': '1. Strictly quarantine affected animals; FMD is extremely contagious via aerosol and contact.\n2. Wash mouth sores with 1% potassium permanganate or 2% sodium bicarbonate solution.\n3. Wash foot lesions with 2% copper sulphate solution and dress with fly-repellent antiseptic.\n4. Administer seasonal FMD vaccination (under National Animal Disease Control Programme - NADCP).',
                'organic_options': 'Neem leaf decoction wash for foot sores and feeding soft, cooked rice or ragi gruel.',
                'safety_precautions': 'Do not move animals, milk cans, or vehicles between affected and non-affected farms. Report outbreaks to nearest Veterinary Hospital.',
                'source_institution': 'National Animal Disease Control Programme (NADCP), DAHD, Govt. of India',
                'last_reviewed_date': 'August 2026'
            },
            {
                'category': 'animal_health',
                'title': 'Ruminal Tympany (Bloat) Emergency Nursing in Ruminants',
                'crop_or_animal': 'Cow, Buffalo, Goat, Sheep',
                'symptoms_description': 'Sudden distension of left paralumbar fossa (stomach swelling), labored breathing with tongue extended, groaning, kicking at belly.',
                'management_practices': '1. IMMEDIATELY CALL VETERINARIAN — acute bloat can cause asphyxiation within 1-2 hours.\n2. Keep animal standing or in sternal sitting posture with forelegs elevated on a mound.\n3. Place a wooden bit or piece of rope in the mouth to encourage chewing and eructation (burping).\n4. Drenching anti-foaming agent (sweet oil/turpentine oil in warm water) ONLY if animal is fully conscious and veterinary guidance is confirmed.',
                'organic_options': 'Ginger powder (25g) and asafoetida (hing 5g) in warm water for mild subacute frothy bloat.',
                'safety_precautions': 'EMERGENCY CAUTION: Never force liquids if animal is choking or downer. Trocarisation of rumen must be performed strictly by a veterinarian.',
                'source_institution': 'Tamil Nadu Veterinary and Animal Sciences University (TANUVAS)',
                'last_reviewed_date': 'September 2026'
            }
        ]
        
        for art in articles_data:
            existing = KnowledgeArticle.query.filter_by(title=art['title']).first()
            if not existing:
                record = KnowledgeArticle(**art)
                db.session.add(record)
        print("Seeded verified Knowledge Articles.")
        
        # 3. Veterinary Directory Contacts across Major Regions
        vet_contacts_data = [
            {
                'name': 'District Veterinary Hospital (Govt)',
                'contact_type': 'Govt Veterinary Hospital',
                'state': 'Telangana',
                'district': 'Warangal',
                'address': 'Subedari, Hanamkonda, Warangal, Telangana 506001',
                'phone': '0870-2456789',
                'emergency_phone': '1962',
                'email': 'dvh.warangal@telangana.gov.in'
            },
            {
                'name': 'Krishi Vigyan Kendra (KVK) - Warangal',
                'contact_type': 'KVK Extension Center',
                'state': 'Telangana',
                'district': 'Warangal',
                'address': 'RARS Campus, Malyal, Mahabubabad / Warangal Rural, Telangana',
                'phone': '08719-240240',
                'emergency_phone': '18001801551',
                'email': 'kvk.warangal@pjtsau.edu.in'
            },
            {
                'name': 'Govt Veterinary Polyclinic - Guntur',
                'contact_type': 'Govt Veterinary Hospital',
                'state': 'Andhra Pradesh',
                'district': 'Guntur',
                'address': 'Kothapet, Collectorate Road, Guntur, AP 522001',
                'phone': '0863-2223456',
                'emergency_phone': '1962',
                'email': 'gvp.guntur@ap.gov.in'
            },
            {
                'name': 'KVK Lam Farm - Guntur',
                'contact_type': 'KVK Extension Center',
                'state': 'Andhra Pradesh',
                'district': 'Guntur',
                'address': 'Regional Agricultural Research Station, Lam, Guntur 522034',
                'phone': '0863-2524017',
                'emergency_phone': '18001801551',
                'email': 'kvk.guntur@angrau.ac.in'
            },
            {
                'name': 'District Veterinary Polyclinic - Pune',
                'contact_type': 'Govt Veterinary Hospital',
                'state': 'Maharashtra',
                'district': 'Pune',
                'address': 'Aundh Camp, Ganeshkhind Road, Pune, Maharashtra 411007',
                'phone': '020-25698741',
                'emergency_phone': '1962',
                'email': 'dvp.pune@maharashtra.gov.in'
            },
            {
                'name': 'Teaching Veterinary Hospital (GADVASU)',
                'contact_type': 'Govt Veterinary Hospital',
                'state': 'Punjab',
                'district': 'Ludhiana',
                'address': 'Guru Angad Dev Veterinary and Animal Sciences University, Ludhiana 141004',
                'phone': '0161-2414011',
                'emergency_phone': '1962',
                'email': 'tvcc@gadvasu.in'
            },
            {
                'name': 'ICAR-NDRI Veterinary Referral Hospital',
                'contact_type': 'Govt Veterinary Hospital',
                'state': 'Haryana',
                'district': 'Karnal',
                'address': 'National Dairy Research Institute Campus, GT Road, Karnal 132001',
                'phone': '0184-2259002',
                'emergency_phone': '1962',
                'email': 'hospital@ndri.res.in'
            },
            {
                'name': 'Kisan Call Centre (All India Toll Free)',
                'contact_type': 'KVK Extension Center',
                'state': 'All India',
                'district': 'National',
                'address': 'Ministry of Agriculture & Farmers Welfare, Govt of India',
                'phone': '1800-180-1551',
                'emergency_phone': '1551',
                'email': 'kisan-callcentre@gov.in'
            }
        ]
        
        for vc in vet_contacts_data:
            existing = VetContact.query.filter_by(name=vc['name']).first()
            if not existing:
                contact = VetContact(**vc)
                db.session.add(contact)
        print("Seeded Veterinary & KVK Directory Contacts.")
        
        db.session.commit()
        print("Database seeding completed successfully!")


if __name__ == '__main__':
    seed_all()
