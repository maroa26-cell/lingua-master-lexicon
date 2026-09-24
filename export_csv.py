import sqlite3
import csv
import os

DB_NAME = "master_lexicon.db"
EXPORT_FILE = "Lexicon_entries.csv"

def main():
    print("=== MASTER LEXICON EXPORT TOOL ===\n")

    # 1. Check if database exists
    if not os.path.exists(DB_NAME):
        print(f"[X] Database '{DB_NAME}' not found!")
        print("    Hakikisha uko ndani ya: C:\\MasterLexicon\\MasterLexicon")
        print("    Kisha run: python create_db.py\n")
        return

    # 2. Connect to database
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # 3. Check if lexicon table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cur.fetchall()]
    if "lexicon" not in tables:
        print("[X] Table 'lexicon' haipo kwenye database.")
        conn.close()
        return

    # 4. Fetch all entries
    cur.execute("SELECT english, swahili, category FROM lexicon")
    rows = cur.fetchall()

    if not rows:
        print("[!] Hakuna entries za ku‑export.")
        conn.close()
        return

    # 5. Export to CSV
    with open(EXPORT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["English", "Swahili", "Category"])
        writer.writerows(rows)

    conn.close()
    print(f"[✔] Export complete! File saved as '{EXPORT_FILE}'")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
