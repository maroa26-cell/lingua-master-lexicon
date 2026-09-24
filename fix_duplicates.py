import sqlite3
import os

DB_NAME = "master_lexicon.db"

def main():
    print("=== MASTER LEXICON DUPLICATE CLEANER ===\n")

    if not os.path.exists(DB_NAME):
        print(f"⚠️ Database '{DB_NAME}' haipatikani!")
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Tafuta duplicates
    cur.execute("""
        SELECT english, COUNT(*) FROM lexicon
        GROUP BY english HAVING COUNT(*) > 1
    """)
    duplicates = cur.fetchall()

    if not duplicates:
        print("✅ Hakuna duplicates zilizopatikana.")
        conn.close()
        return

    print(f"🔁 Duplicates {len(duplicates)} zimepatikana:\n")
    for eng, count in duplicates:
        print(f"  - {eng} (x{count})")

    # Futa duplicates na kubakiza entry moja
    for eng, _ in duplicates:
        cur.execute("""
            DELETE FROM lexicon
            WHERE english = ?
            AND rowid NOT IN (
                SELECT MIN(rowid) FROM lexicon WHERE english = ?
            )
        """, (eng, eng))

    conn.commit()
    conn.close()

    print("\n[✔] Duplicates zote zimeondolewa — entry moja imebakizwa kwa kila neno.")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
