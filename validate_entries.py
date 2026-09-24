import sqlite3
import os
import re

DB_NAME = "master_lexicon.db"

# Ruhusu herufi, namba, space, dash, apostrophe
VALID_PATTERN = re.compile(r"^[A-Za-z0-9 '\-]+$")

def validate_text(text):
    if not text.strip():
        return "Empty field"
    if not VALID_PATTERN.match(text):
        return "Invalid characters"
    if "  " in text:
        return "Multiple spaces"
    return None

def main():
    print("=== MASTER LEXICON VALIDATION TOOL ===\n")

    if not os.path.exists(DB_NAME):
        print(f"⚠️ Database '{DB_NAME}' haipatikani!")
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT english, swahili, category FROM lexicon")
    rows = cur.fetchall()
    conn.close()

    errors = []

    for i, (eng, swa, cat) in enumerate(rows, start=1):
        eng_err = validate_text(eng)
        swa_err = validate_text(swa)
        cat_err = validate_text(cat)

        if eng_err or swa_err or cat_err:
            errors.append({
                "line": i,
                "english": eng,
                "swahili": swa,
                "category": cat,
                "errors": {
                    "english": eng_err,
                    "swahili": swa_err,
                    "category": cat_err
                }
            })

    if not errors:
        print("✅ Entries zote ni sahihi — hakuna makosa.")
    else:
        print(f"⚠️ Makosa {len(errors)} yamepatikana:\n")
        for err in errors:
            print(f"Mstari {err['line']}:")
            print(f"  English : {err['english']}  → {err['errors']['english']}")
            print(f"  Swahili : {err['swahili']}  → {err['errors']['swahili']}")
            print(f"  Category: {err['category']}  → {err['errors']['category']}")
            print("-" * 60)

    print("\n=== DONE ===")
