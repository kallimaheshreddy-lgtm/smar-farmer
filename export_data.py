"""
Export SMART FARMER AI database tables and summary to readable files.
"""
import os
import sys
import sqlite3
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "faemer.db"
OUTPUT_DIR = BASE_DIR / "database_data"
REPORT_FILE = BASE_DIR / "database_report.txt"
DESKTOP_REPORT = Path(os.environ.get("USERPROFILE", "")) / "OneDrive" / "Desktop" / "Smart_Farmer_Database_Report.txt"

def export_all():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row["name"] for row in cur.fetchall() if not row["name"].startswith("sqlite_")]

    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("  SMART FARMER AI - COMPLETE DATABASE REPORT")
    report_lines.append(f"  Database File: {DB_PATH}")
    report_lines.append("=" * 70)
    report_lines.append("")

    report_lines.append(f"[SUMMARY OF TABLES] ({len(tables)} tables):")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) as cnt FROM {t}")
        cnt = cur.fetchone()["cnt"]
        report_lines.append(f"  - {t:<30}: {cnt} records")
    report_lines.append("")

    # Export each table to CSV
    for t in tables:
        cur.execute(f"SELECT * FROM {t}")
        rows = cur.fetchall()
        csv_path = OUTPUT_DIR / f"{t}.csv"
        
        if rows:
            col_names = [col[0] for col in cur.description]
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(col_names)
                for r in rows:
                    writer.writerow([r[c] for c in col_names])

    # Detailed section: Users
    report_lines.append("-" * 70)
    report_lines.append("[REGISTERED USERS & FARMERS]:")
    cur.execute("SELECT id, name, phone, email, is_admin, preferred_language, created_at FROM users")
    for u in cur.fetchall():
        role = "ADMIN" if u["is_admin"] else "FARMER"
        report_lines.append(f"  ID: {u['id']} | Name: {u['name']} | Phone: {u['phone']} | Email: {u['email']} | Role: {role} | Lang: {u['preferred_language']}")
    report_lines.append("")

    # Detailed section: Plant Assessments
    report_lines.append("-" * 70)
    report_lines.append("[PLANT HEALTH ASSESSMENTS]:")
    cur.execute("SELECT id, user_id, crop_type, detected_issue, confidence, created_at FROM plant_assessments ORDER BY id DESC")
    plant_rows = cur.fetchall()
    if plant_rows:
        for p in plant_rows:
            report_lines.append(f"  ID: {p['id']} | Farmer ID: {p['user_id']} | Crop: {p['crop_type']} | Issue: {p['detected_issue']} | Confidence: {p['confidence']} | Date: {p['created_at']}")
    else:
        report_lines.append("  (No plant health assessments recorded yet)")
    report_lines.append("")

    # Detailed section: Animal Health Triage
    report_lines.append("-" * 70)
    report_lines.append("[ANIMAL HEALTH TRIAGE RECORDS]:")
    cur.execute("SELECT id, user_id, species, urgency_level, requires_immediate_vet, created_at FROM animal_triage_records ORDER BY id DESC")
    animal_rows = cur.fetchall()
    if animal_rows:
        for a in animal_rows:
            vet_flag = "CALL EMERGENCY 1962" if a["requires_immediate_vet"] else "Routine Care"
            report_lines.append(f"  ID: {a['id']} | Farmer ID: {a['user_id']} | Species: {a['species']} | Urgency: {a['urgency_level'].upper()} ({vet_flag}) | Date: {a['created_at']}")
    else:
        report_lines.append("  (No animal triage records recorded yet)")
    report_lines.append("")

    # Detailed section: Vet Contacts
    report_lines.append("-" * 70)
    report_lines.append("[VETERINARY & KVK CONTACT DIRECTORY]:")
    cur.execute("SELECT id, name, contact_type, district, state, phone, emergency_phone FROM vet_contacts")
    for v in cur.fetchall():
        contact = v['phone'] or v['emergency_phone'] or 'N/A'
        report_lines.append(f"  - {v['name']} ({v['contact_type']}) | {v['district']}, {v['state']} | Tel: {contact}")
    report_lines.append("")

    # Detailed section: Knowledge Articles
    report_lines.append("-" * 70)
    report_lines.append("[KNOWLEDGE BASE ARTICLES]:")
    cur.execute("SELECT id, title, category, crop_or_animal, source_institution FROM knowledge_articles")
    for k in cur.fetchall():
        report_lines.append(f"  ID: {k['id']} | Title: {k['title']} | Category: {k['category']} | Target: {k['crop_or_animal']} | Source: {k['source_institution']}")
    report_lines.append("")
    report_lines.append("=" * 70)

    report_text = "\n".join(report_lines)

    # Save to faemer/database_report.txt
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"[OK] Saved report to: {REPORT_FILE}")

    # Also save copy to Desktop
    try:
        with open(DESKTOP_REPORT, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"[OK] Saved desktop copy to: {DESKTOP_REPORT}")
    except Exception as e:
        print(f"[NOTE] Could not write directly to Desktop: {e}")

    con.close()
    print(f"[OK] Exported all CSV tables into: {OUTPUT_DIR}")

if __name__ == "__main__":
    export_all()
