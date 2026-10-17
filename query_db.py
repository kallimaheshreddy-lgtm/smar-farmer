"""
Interactive SQL Console for SMART FARMER AI (faemer.db)
"""
import sqlite3
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB_PATH = os.path.join(os.path.dirname(__file__), 'faemer.db')

def run_query_console():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database file '{DB_PATH}' was not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 60)
    print("  SMART FARMER AI - INTERACTIVE SQL TERMINAL")
    print(f"  Connected to: {DB_PATH}")
    print("=" * 60)
    print("Commands:")
    print("  tables        - List all tables in the database")
    print("  schema <table>- View columns of a specific table")
    print("  exit / quit   - Close database connection and exit")
    print("  Or type any SQL query (e.g. SELECT * FROM users;)")
    print("-" * 60)

    while True:
        try:
            cmd = input("\nSQL> ").strip()
            if not cmd:
                continue

            if cmd.lower() in ('exit', 'quit', 'q'):
                print("Disconnected from database. Goodbye!")
                break

            if cmd.lower() == 'tables':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
                tbls = cursor.fetchall()
                print("\n[TABLES IN DATABASE]:")
                for t in tbls:
                    cursor.execute(f"SELECT COUNT(*) FROM {t[0]}")
                    cnt = cursor.fetchone()[0]
                    print(f"  * {t[0]:<25} ({cnt} rows)")
                continue

            if cmd.lower().startswith('schema'):
                parts = cmd.split()
                if len(parts) > 1:
                    tname = parts[1]
                    cursor.execute(f"PRAGMA table_info({tname});")
                    cols = cursor.fetchall()
                    if cols:
                        print(f"\n[SCHEMA FOR '{tname}']:")
                        for c in cols:
                            pk = " [PRIMARY KEY]" if c[5] else ""
                            print(f"  - {c[1]:<20} ({c[2]}){pk}")
                    else:
                        print(f"Table '{tname}' not found.")
                else:
                    print("Usage: schema <table_name>")
                continue

            # Execute SQL Query
            cursor.execute(cmd)
            if cmd.strip().lower().startswith(('insert', 'update', 'delete', 'create', 'drop', 'alter')):
                conn.commit()
                print(f"[OK] Query executed successfully ({cursor.rowcount} row(s) affected).")
            else:
                rows = cursor.fetchall()
                if cursor.description:
                    col_names = [d[0] for d in cursor.description]
                    print("-" * 60)
                    print(" | ".join(col_names))
                    print("-" * 60)
                    for r in rows:
                        print(" | ".join(str(val) for val in r))
                    print(f"\n({len(rows)} row(s) returned)")
                else:
                    print("[OK] Query executed successfully.")

        except Exception as e:
            print(f"[SQL ERROR]: {e}")

    conn.close()

if __name__ == '__main__':
    run_query_console()
