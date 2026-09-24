import sqlite3
import json
import os

DB_NAME = "master_lexicon.db"
EXPORT_FILE = "Lexicon_entries.json"

def main():
    print("=== MASTER LEXICON JSON EXPORT TOOL ===\n")

    if not os.path.exists(DB_NAME):
        print(f"⚠️ Database '{DB_NAME}' haipatikani!")
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT english, swahili, category FROM lexicon")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("⚠️ Hakuna entries za ku‑export.")
        return

    # Convert to JSON structure
    data = [
        {"English": eng, "Swahili": swa, "Category": cat}
        for eng, swa, cat in rows
    ]

    with open(EXPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"[✔] Export complete! File saved as '{EXPORT_FILE}'")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
