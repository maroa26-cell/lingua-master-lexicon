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

def sync_db(csv_rows, db_rows):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Add missing entries
    added = [r for r in csv_rows if r not in db_rows]
    for r in added:
        cur.execute("INSERT INTO lexicon (english, swahili, category) VALUES (?, ?, ?)", r)

    # Remove extra entries
    removed = [r for r in db_rows if r not in csv_rows]
    for r in removed:
        cur.execute("DELETE FROM lexicon WHERE english=? AND swahili=? AND category=?", r)

    conn.commit()
    conn.close()
    return added, removed

print("=== MASTER LEXICON SYNC TOOL ===\n")

csv_rows = read_csv(CSV_FILE)
db_rows = read_db(DB_NAME)

added, removed = sync_db(csv_rows, db_rows)

print(f"📊 CSV entries: {len(csv_rows)}")
print(f"🗄️ DB entries : {len(db_rows)}\n")

if not added and not removed:
    print("✅ Database na CSV zimesawazishwa kikamilifu — hakuna mabadiliko.")
else:
    if added:
        print(f"➕ {len(added)} entries zimeongezwa kutoka CSV.")
    if removed:
        print(f"➖ {len(removed)} entries zimeondolewa kutoka database.")

print("\n=== DONE ===")
