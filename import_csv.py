import sqlite3
import csv
import os

DB_NAME = "master_lexicon.db"
CSV_FILE = "Lexicon_entries.csv"

def main():
    print("=== MASTER LEXICON IMPORT TOOL ===\n")

    # 1. Check if database exists
    if not os.path.exists(DB_NAME):
        print(f"[X] Database '{DB_NAME}' not found!")
        print("    Hakikisha uko ndani ya: C:\\MasterLexicon\\MasterLexicon")
        return

    # 2. Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"[X] CSV file '{CSV_FILE}' not found!")
        print("    Hakikisha ume‑export data kwanza (python export_csv.py)")
        return

    # 3. Connect to database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # 4. Check if lexicon table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cur.fetchall()]
    if "lexicon" not in tables:
        print("[X] Table 'lexicon' haipo kwenye database.")
        conn.close()
        return

    # 5. Read CSV file
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        rows = [row for row in reader]

    # 6. Insert entries
    cur.executemany("INSERT INTO lexicon (english, swahili, category) VALUES (?, ?, ?)", rows)
    conn.commit()
    conn.close()

    print(f"[✔] {len(rows)} entries zime‑importiwa kutoka '{CSV_FILE}' kwenye database.")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
