import os
import sqlite3
import json
import csv

DB_NAME = "master_lexicon.db"
CSV_FILE = "Lexicon_entries.csv"
JSON_FILE = "Lexicon_entries.json"
SQL_FILE = "master_lexicon_dump.sql"
BACKUP_FOLDER = "backups"

SCRIPTS = [
    "check_db.py", "insert_sample.py", "export_csv.py", "backup_db.py",
    "restore_backup.py", "clear_db.py", "import_csv.py", "compare_db_csv.py",
    "sync_db_csv.py", "search_lexicon.py", "stats_lexicon.py", "export_json.py",
    "merge_csv_db.py", "validate_entries.py", "fix_duplicates.py",
    "normalize_entries.py", "export_sql.py", "import_sql.py",
    "auto_backup.py", "auto_restore.py", "auto_start.py"
]

def check_file(path):
    return os.path.exists(path)

def check_db():
    if not check_file(DB_NAME):
        return False, 0
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM lexicon")
    count = cur.fetchone()[0]
    conn.close()
    return True, count

def check_csv():
    if not check_file(CSV_FILE):
        return False, 0
    with open(CSV_FILE, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        return True, sum(1 for _ in reader)

def check_json():
    if not check_file(JSON_FILE):
        return False, 0
    with open(JSON_FILE, encoding="utf-8") as f:
        data = json.load(f)
        return True, len(data)

def check_sql():
    return check_file(SQL_FILE)

def check_backups():
    if not os.path.exists(BACKUP_FOLDER):
        return False, None
    backups = [f for f in os.listdir(BACKUP_FOLDER) if f.endswith(".db")]
    if not backups:
        return False, None
    backups.sort(reverse=True)
    return True, backups[0]

def check_scripts():
    missing = [s for s in SCRIPTS if not check_file(s)]
    return missing

def main():
    print("=== MASTER LEXICON SYSTEM HEALTH CHECK ===\n")

    score = 100

    # Database
    db_ok, db_count = check_db()
    print(f"📁 Database: {'OK' if db_ok else 'MISSING'} ({db_count} entries)")
    if not db_ok: score -= 20

    # CSV
    csv_ok, csv_count = check_csv()
    print(f"📄 CSV: {'OK' if csv_ok else 'MISSING'} ({csv_count} entries)")
    if not csv_ok: score -= 10

    # JSON
    json_ok, json_count = check_json()
    print(f"📄 JSON: {'OK' if json_ok else 'MISSING'} ({json_count} entries)")
    if not json_ok: score -= 10

    # SQL dump
    sql_ok = check_sql()
    print(f"🗄️ SQL Dump: {'OK' if sql_ok else 'MISSING'}")
    if not sql_ok: score -= 10

    # Backups
    backup_ok, latest_backup = check_backups()
    print(f"📦 Backups: {'OK' if backup_ok else 'NONE'}")
    if backup_ok:
        print(f"   Latest: {latest_backup}")
    else:
        score -= 10

    # Scripts
    missing_scripts = check_scripts()
    print(f"🧩 Scripts: {'ALL PRESENT' if not missing_scripts else 'MISSING'}")
    if missing_scripts:
        for s in missing_scripts:
            print(f"   ❌ {s}")
        score -= len(missing_scripts)

    # Consistency check
    if db_ok and csv_ok and json_ok:
        if db_count == csv_count == json_count:
            print("🔁 Consistency: OK (DB = CSV = JSON)")
        else:
            print("⚠️ Consistency: MISMATCH")
            score -= 10

    # Final score
    print(f"\n💯 SYSTEM HEALTH SCORE: {score}/100")

    if score == 100:
        print("✅ System is PERFECT — production ready.")
    elif score >= 80:
        print("🟢 System is HEALTHY — minor issues only.")
    elif score >= 60:
        print("🟡 System is FAIR — needs attention.")
    else:
        print("🔴 System is UNHEALTHY — critical issues detected.")

    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
