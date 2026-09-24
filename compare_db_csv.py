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
        return list(reader)

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

print("=== COMPARE DATABASE vs CSV ===\n")

csv_rows = read_csv(CSV_FILE)
db_rows = read_db(DB_NAME)

print(f"CSV rows: {len(csv_rows)}")
print(f"DB rows : {len(db_rows)}\n")

# Compare counts
if len(csv_rows) != len(db_rows):
    print("⚠️ Idadi ya entries inatofautiana kati ya database na CSV.\n")

# Compare content
differences = []
for i, (csv_row, db_row) in enumerate(zip(csv_rows, db_rows), start=1):
    if tuple(csv_row) != tuple(db_row):
        differences.append((i, csv_row, db_row))

if differences:
    print("🔍 Tofauti zimepatikana:\n")
    for line, csv_r, db_r in differences:
        print(f"Mstari {line}:")
        print(f"CSV: {csv_r}")
        print(f"DB : {db_r}")
        print("-" * 80)
else:
    print("✅ Database na CSV zinafanana kikamilifu.")

print("\n=== DONE ===")
