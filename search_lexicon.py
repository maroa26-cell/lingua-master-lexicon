import sqlite3
import sys
import os

DB_NAME = "master_lexicon.db"

def search_word(word):
    if not os.path.exists(DB_NAME):
        print(f"⚠️ Database '{DB_NAME}' haipatikani!")
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Tafuta kwa English au Swahili
    cur.execute("""
        SELECT english, swahili, category
        FROM lexicon
        WHERE english LIKE ? OR swahili LIKE ?
    """, (f"%{word}%", f"%{word}%"))

    results = cur.fetchall()
    conn.close()

    return results

def main():
    if len(sys.argv) < 2:
        print("⚠️ Tafadhali andika neno la kutafuta.")
        print("Mfano: python search_lexicon.py Hello")
        return

    word = sys.argv[1]
    print(f"=== SEARCH RESULTS FOR: '{word}' ===\n")

    results = search_word(word)

    if not results:
        print("❌ Hakuna matokeo yaliyopatikana.")
        return

    for eng, swa, cat in results:
        print(f"English : {eng}")
        print(f"Swahili : {swa}")
        print(f"Category: {cat}")
        print("-" * 40)

    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
