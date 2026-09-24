import sqlite3
import os

DB_NAME = "master_lexicon.db"
IMPORT_FILE = "master_lexicon_dump.sql"

def main():
    print("=== MASTER LEXICON SQL IMPORT TOOL ===\n")

    if not os.path.exists(IMPORT_FILE):
        print(f"⚠️ Faili '{IMPORT_FILE}' haipatikani!")
        return

    # Ikiwa database ipo, toa tahadhari
    if os.path.exists(DB_NAME):
        print(f"⚠️ Database '{DB_NAME}' ipo tayari.")
        confirm = input("Unataka kuireplace? (andika YES kuthibitisha): ")
        if confirm.strip().upper() != "YES":
            print("❌ Operation imekatishwa — database haijabadilishwa.")
            return
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    with open(IMPORT_FILE, "r", encoding="utf-8") as f:
        sql_script = f.read()

    cur.executescript(sql_script)
    conn.commit()
    conn.close()

    print(f"[✔] Database '{DB_NAME}' imeundwa upya kutoka '{IMPORT_FILE}'.")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
