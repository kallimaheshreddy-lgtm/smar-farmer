"""
Database Inspector for SMART FARMER AI (faemer.db)
"""
import sqlite3
import os
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB_PATH = os.path.join(os.path.dirname(__file__), 'faemer.db')

def inspect():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    print("=" * 65)
    print("  SMART FARMER AI - SQLITE DATABASE VIEWER")
    print(f"  File: {DB_PATH}")
    print("=" * 65)

    # List tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = [row[0] for row in cur.fetchall()]
    print(f"\n[TABLES IN DATABASE] ({len(tables)} tables):")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        count = cur.fetchone()[0]
        print(f"  * {t:<28} : {count} records")

    # Show Users
    print("\n" + "-" * 65)
    print("[REGISTERED FARMERS & USERS]:")
    cur.execute("SELECT id, name, phone, email, is_admin FROM users LIMIT 10")
    users = cur.fetchall()
    for u in users:
        role = "ADMIN" if u[4] else "FARMER"
        print(f"  ID: {u[0]} | Name: {u[1]} | Phone: {u[2]} | Role: {role}")

    # Show Recent Plant Assessments
    print("\n" + "-" * 65)
    print("[RECENT PLANT HEALTH ASSESSMENTS]:")
    cur.execute("SELECT id, crop_type, detected_issue, confidence, created_at FROM plant_assessments ORDER BY id DESC LIMIT 5")
    plants = cur.fetchall()
    if plants:
        for p in plants:
            print(f"  ID: {p[0]} | Crop: {p[1]} | Issue: {p[2]} | Confidence: {p[3]} | Time: {p[4]}")
    else:
        print("  (No plant assessments saved yet)")

    # Show Recent Animal Triage Records
    print("\n" + "-" * 65)
    print("[RECENT ANIMAL HEALTH TRIAGE RECORDS]:")
    cur.execute("SELECT id, species, urgency_level, requires_immediate_vet, created_at FROM animal_triage_records ORDER BY id DESC LIMIT 5")
    animals = cur.fetchall()
    if animals:
        for a in animals:
            vet_flag = "CALL 1962" if a[3] else "Routine"
            print(f"  ID: {a[0]} | Species: {a[1]} | Urgency: {a[2].upper()} ({vet_flag}) | Time: {a[4]}")
    else:
        print("  (No animal triage records saved yet)")

    print("\n" + "=" * 65)
    con.close()

if __name__ == '__main__':
    inspect()
