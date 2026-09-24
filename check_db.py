import os
import sqlite3

DB_NAME = "master_lexicon.db"

def main():
    print("=== MASTER LEXICON DATABASE CHECK ===\n")

    # 1. Check if database file exists
    if not os.path.exists(DB_NAME):
        print(f"[X] Database file '{DB_NAME}' NOT FOUND in current folder.")
        print("    Hakikisha uko ndani ya: C:\\MasterLexicon\\MasterLexicon")
        print("    Kisha run: python create_db.py\n")
        return
    else:
        print(f"[✔] Database file '{DB_NAME}' found.\n")

    # 2. Connect to database
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    except Exception as e:
        print("[X] Failed to connect to database:")
        print(e)
        return

    # 3. List tables
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row["name"] for row in cur.fetchall()]

    print("[✔] Tables found in database:")
    for t in tables:
        print(f"    - {t}")
    print()

    # 4. Check required tables
    required = ["admin", "lexicon"]
    for r in required:
        if r in tables:
            print(f"[✔] Required table '{r}' exists.")
        else:
            print(f"[X] Required table '{r}' is MISSING!")
    print()

    # 5. Count entries in lexicon
    if "lexicon" in tables:
        cur.execute("SELECT COUNT(*) AS cnt FROM lexicon")
        count = cur.fetchone()["cnt"]
        print(f"[✔] Lexicon entries count: {count}")
    else:
        print("[X] Cannot count entries — 'lexicon' table missing.")

    conn.close()
    print("\n=== CHECK COMPLETE ===")

if __name__ == "__main__":
    main()
