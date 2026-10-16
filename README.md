# SMART FARMER AI — Smart Farming and Animal Health Assistant for Indian Farmers

A production-ready web application designed specifically for Indian farmers and livestock keepers with modular AI integration, verified agronomic guidance, conservative veterinary triage, and multilingual support (English, తెలుగు, हिन्दी).

---

## 🌟 Key Features

1. **🌾 Plant Disease & Health Checker**
   - Upload clear photos of affected crops or select visible symptoms.
   - Dual AI & Agronomic Engine: Integrates with genuine deep learning inference APIs, and gracefully falls back to verified ICAR / State Agricultural University (TNAU, ANGRAU) diagnostic keys when models are unconfigured.
   - Provides verified Integrated Pest Management (IPM), biological biocontrols, safety precautions, and source citations.
   - Never fabricates AI predictions or prescribes unverified pesticides.

2. **🐄 Conservative Animal Health Triage**
   - Covers Cows, Buffaloes, Goats, Sheep, Poultry, and working livestock.
   - Categorizes cases into **CRITICAL EMERGENCY** (Red), **URGENT** (Yellow/Orange), and **MONITOR & SAFE CARE** (Green).
   - Flags danger signs (severe bloat, recumbency/downer cows, convulsions, foaming, bleeding).
   - Strict Veterinary Ethics: The system strictly avoids prescribing antibiotics or injections, providing safe interim first-aid and direct links to emergency helplines.

3. **📚 Trustworthy Agricultural & Veterinary Knowledge Base**
   - Searchable repository of crop diseases, insect pests, and scientific fertilizer schedules.
   - Cites recognized Indian institutions: ICAR institutes, IVRI, ANGRAU, TNAU, and DAHD with last review dates.
   - Administrator dashboard allows reviewing, updating, and deactivating outdated entries.

4. **🚜 My Farm Management (Multi-Tenant & Isolated)**
   - Manage field plots, crop varieties, planting dates, and expected harvest dates.
   - Track field operations (irrigation, fertilizer, spraying) and farm expenses.
   - Strict data isolation ensuring each farmer only accesses their own private records.

5. **🐾 Animal Herd Records & Veterinary Visits**
   - Maintain animal profiles (Tag ID, breed, age, gender, reproductive & health status).
   - Log veterinary consultations, prescribed doctor notes, and follow-up schedules.

6. **🌦️ Agro-Climatic Weather Dashboard**
   - Supports live OpenWeatherMap API with transparent configuration fallback (no invented numbers).
   - Manual district selector covering Indian states with regional agro-climatic advisories.
   - Automated foliar spraying safety windows and livestock heat/cold stress guidance.

7. **🏥 Veterinary & KVK Contact Directory**
   - Directory of Government Veterinary Hospitals, Polyclinics, and Krishi Vigyan Kendras.
   - Instant click-to-call links and direct emergency hotline access (National Animal Helpline: 1962, Kisan Call Centre: 1800-180-1551).

8. **🌐 Multilingual Localization**
   - Full translation support for **English**, **Telugu (తెలుగు)**, and **Hindi (हिन्दी)** with an interactive dialect switcher.

---

## 🏗️ Project Architecture

```
faemer/
├── app/
│   ├── __init__.py               # Flask application factory, extensions & error handlers
│   ├── models.py                 # SQLAlchemy models (User, Crop, Livestock, Triage, KB, Vets)
│   ├── translations.py           # Compatibility translation wrapper
│   ├── blueprints/               # Modular Flask Blueprints
│   │   ├── main.py               # Landing page, dashboard, healthz, language toggle
│   │   ├── auth.py               # Login, registration, password hashing, profile
│   │   ├── plant.py              # Plant checker & history
│   │   ├── animal.py             # Animal triage & history
│   │   ├── farm.py               # Crops, field operations & expenses
│   │   ├── livestock.py          # Animal records & vet visits
│   │   ├── knowledge.py          # Knowledge base & guides
│   │   ├── weather.py            # Weather dashboard & advisories
│   │   ├── vets.py               # Veterinary contacts directory
│   │   └── admin.py              # Administrator curation portal
│   ├── services/                 # Reusable business logic
│   │   ├── plant_service.py      # Plant AI adapter & agronomic symptom diagnostic keys
│   │   ├── animal_service.py     # Conservative veterinary triage & danger signs
│   │   ├── weather_service.py    # OpenWeatherMap client & agro-advisories
│   │   ├── knowledge_service.py  # Knowledge queries & citations
│   │   └── i18n_service.py       # English, Telugu, and Hindi translations
│   ├── static/
│   │   ├── css/styles.css        # Custom agricultural design system
│   │   ├── js/main.js            # Image preview, geolocation & triage alerts
│   │   └── uploads/              # Isolated upload directory
│   └── templates/                # Jinja2 templates for all views
├── tests/                        # Automated Pytest suite (31 tests)
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_data_isolation.py
│   ├── test_plant_assessment.py
│   ├── test_animal_triage.py
│   ├── test_weather_service.py
│   ├── test_knowledge_base.py
│   └── test_routes_and_security.py
├── .env.example                  # Environment configuration template
├── Procfile                      # Render start command
├── render.yaml                   # Render Blueprint with managed PostgreSQL
├── requirements.txt              # Pinned production dependencies
├── seed_data.py                  # Verified database seeder
└── run.py                        # Local development runner
```

---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Git

### 2. Setup Virtual Environment
```bash
# Clone the repository and navigate into it
cd faemer

# Create and activate virtual environment
python -m venv .venv

# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# On Linux/macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy template configuration
cp .env.example .env
```

### 5. Initialize & Seed Database
```bash
python seed_data.py
```
This automatically creates the database schema and seeds initial verified ICAR agricultural guides, veterinary contacts, and demo accounts:
- **Admin**: `admin@smartfarmer.org` / `AdminFarmer@2026`
- **Farmer**: `farmer@smartfarmer.org` / `Farmer@2026`

### 6. Run the Application
```bash
python run.py
```
Open your browser at **http://127.0.0.1:5000**.

---

## 🧪 Running Automated Tests

The application includes 31 unit and integration tests covering authentication, multi-tenant data isolation, image verification, AI fallback, veterinary triage, weather fallback, and admin security:

```bash
python -m pytest tests -v
```

All 31 tests pass with 100% success rate.

---

## ⚙️ External Service Integrations

### 1. Configuring Real Plant Disease AI Models
The application uses the `PlantDiseaseModelInterface` and `RemoteModelAdapter` pattern in `app/services/plant_service.py`.
To connect an automated classification model (e.g. PyTorch/TensorFlow/FastAPI service or HuggingFace):
1. In your `.env` or Render environment settings, specify:
   ```env
   MODEL_API_URL=https://your-model-api-endpoint.com/predict
   MODEL_API_KEY=your_optional_bearer_token
   ```
2. The endpoint receives a multipart `POST` with `file`, `crop_type`, and `symptoms`, returning JSON predictions:
   ```json
   {
     "predictions": [{"label": "Rice Blast", "confidence": 0.94}],
     "notes": "Spindle-shaped foliar lesion detected."
   }
   ```
3. If `MODEL_API_URL` is omitted, the application transparently runs verified ICAR/University diagnostic keys and clearly labels the output as manual agronomic screening.

### 2. Configuring Real-Time Weather
1. Register for a free account at [OpenWeatherMap](https://openweathermap.org/api).
2. Generate an API Key.
3. Add it to your `.env` file:
   ```env
   WEATHER_API_KEY=your_actual_api_key_here
   ```
4. If unconfigured, the application presents an informative setup guide and displays regional agro-climatic baseline advisories for the chosen Indian district without fabricating temperatures.

---

## 🌐 Render Deployment Guide

1. **Push to GitHub**:
   Commit and push your repository to GitHub.

2. **Deploy via Render Blueprint**:
   - Log into [Render Dashboard](https://dashboard.render.com/).
   - Click **New** > **Blueprint**.
   - Connect your GitHub repository.
   - Render will read `render.yaml` and provision:
     * A web service running `python -m gunicorn run:app`
     * A managed PostgreSQL database (`smartfarmer-db`)
     * Automatic database seeding via `seed_data.py`.

3. **Deploy Manually (Alternative)**:
   - Create a **Web Service** on Render.
   - **Environment**: Python
   - **Build Command**: `python -m pip install -r requirements.txt && python seed_data.py`
   - **Start Command**: `python -m gunicorn run:app`
   - **Environment Variables**:
     * `FLASK_ENV`: `production`
     * `SECRET_KEY`: (Click Generate)
     * `DATABASE_URL`: (Paste PostgreSQL connection string)
   - **Health Check Path**: `/healthz`

Production startup requires a non-empty `SECRET_KEY`; the application will stop
with a clear error if it is missing. Generate a value with
`python -c "import secrets; print(secrets.token_hex(32))"` and set it as a
Render environment variable. PostgreSQL connection URLs use the `psycopg` 3
binary driver, which supports Windows development systems as well.

---

## ⚖️ Ethical Safeguards & Legal Disclaimers

- **Preliminary Screening**: Image analysis and symptom checklists are designed to assist farmers with early screening. They do not replace on-site physical diagnosis by certified Krishi Vigyan Kendra (KVK) officers or licensed agronomists.
- **Strict Veterinary Standard**: In strict accordance with veterinary regulations, Smart Farmer AI **does not prescribe antibiotics, scheduled prescription drugs, or injections**. Clinical prescriptions must only be issued by registered veterinary practitioners. In all urgent situations, farmers are directed to contact their nearest veterinary dispensary or dial the National Animal Helpline at **1962**.
