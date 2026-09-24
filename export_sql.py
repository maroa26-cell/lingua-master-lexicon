import sqlite3
import os

DB_NAME = "master_lexicon.db"
EXPORT_FILE = "master_lexicon_dump.sql"

def main():
    print("=== MASTER LEXICON SQL EXPORT TOOL ===\n")

    if not os.path.exists(DB_NAME):
        print(f"⚠️ Database '{DB_NAME}' haipatikani!")
        return

    conn = sqlite3.connect(DB_NAME)
    with open(EXPORT_FILE, "w", encoding="utf-8") as f:
        for line in conn.iterdump():
            f.write(f"{line}\n")
    conn.close()

    print(f"[✔] Export complete! File saved as '{EXPORT_FILE}'")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
