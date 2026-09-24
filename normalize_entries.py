import sqlite3
import os
import re

DB_NAME = "master_lexicon.db"

def normalize_text(text, mode="default"):
    # Ondoa spaces zisizohitajika
    text = text.strip()
    # Badilisha spaces nyingi kuwa moja
    text = re.sub(r"\s+", " ", text)

    if mode == "english" or mode == "swahili":
        # Herufi ya kwanza kubwa, zingine ndogo
        text = text.title()
    elif mode == "category":
        # Category iwe lowercase
        text = text.lower()

    return text

def main():
    print("=== MASTER LEXICON NORMALIZATION TOOL ===\n")

    if not os.path.exists(DB_NAME):
        print(f"⚠️ Database '{DB_NAME}' haipatikani!")
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT rowid, english, swahili, category FROM lexicon")
    rows = cur.fetchall()

    updated_count = 0

    for rowid, eng, swa, cat in rows:
        new_eng = normalize_text(eng, "english")
        new_swa = normalize_text(swa, "swahili")
        new_cat = normalize_text(cat, "category")

        if (new_eng, new_swa, new_cat) != (eng, swa, cat):
            cur.execute("""
                UPDATE lexicon
                SET english = ?, swahili = ?, category = ?
                WHERE rowid = ?
            """, (new_eng, new_swa, new_cat, rowid))
            updated_count += 1

    conn.commit()
    conn.close()

    print(f"[✔] {updated_count} entries zimesafishwa na kurekebishwa.")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
