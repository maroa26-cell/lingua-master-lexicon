import sqlite3
import os

DB_NAME = "master_lexicon.db"

def main():
    print("=== MASTER LEXICON CLEAR TOOL ===\n")

    # 1. Check if database exists
    if not os.path.exists(DB_NAME):
        print(f"[X] Database '{DB_NAME}' not found!")
        print("    Hakikisha uko ndani ya: C:\\MasterLexicon\\MasterLexicon")
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

    # 4. Confirm deletion
    confirm = input("⚠️ Unataka kufuta entries zote? (andika YES kuthibitisha): ")
    if confirm.strip().upper() != "YES":
        print("[!] Operation cancelled.")
        conn.close()
        return

    # 5. Delete all entries
    cur.execute("DELETE FROM lexicon")
    conn.commit()
    conn.close()

    print("[✔] Entries zote zimefutwa kutoka 'lexicon' table.")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
