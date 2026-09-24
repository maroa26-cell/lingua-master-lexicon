import sqlite3
import csv
import os

DB_NAME = "master_lexicon.db"
CSV_FILE = "Lexicon_entries.csv"

def read_csv(path):
    if not os.path.exists(path):
        print(f"⚠️ Faili haipatikani: {path}")
        return []
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        return [tuple(row) for row in reader]

def read_db(path):
    if not os.path.exists(path):
        print(f"⚠️ Database haipatikani: {path}")
        return []
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute("SELECT english, swahili, category FROM lexicon")
    rows = cur.fetchall()
    conn.close()
    return rows

def merge_data(csv_rows, db_rows):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    added = []
    skipped = []

    for row in csv_rows:
        if row not in db_rows:
            cur.execute("INSERT INTO lexicon (english, swahili, category) VALUES (?, ?, ?)", row)
            added.append(row)
        else:
            skipped.append(row)

    conn.commit()
    conn.close()
    return added, skipped

print("=== MASTER LEXICON MERGE TOOL ===\n")

csv_rows = read_csv(CSV_FILE)
db_rows = read_db(DB_NAME)

added, skipped = merge_data(csv_rows, db_rows)

print(f"📊 CSV entries: {len(csv_rows)}")
print(f"🗄️ DB entries : {len(db_rows)}\n")

if added:
    print(f"➕ {len(added)} entries zimeongezwa kutoka CSV.")
else:
    print("✅ Hakuna entries mpya za kuongeza.")

if skipped:
    print(f"⏩ {len(skipped)} entries zilikuwepo tayari kwenye database.")

print("\n=== DONE ===")
