import sqlite3
import os

DB_NAME = "master_lexicon.db"

def get_stats():
    # Kama database haipo, rudisha data tupu
    if not os.path.exists(DB_NAME):
        return {
            "total_entries": 0,
            "distinct_categories": 0,
            "empty_entries": 0,
            "duplicates": []
        }

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # 1️⃣ Idadi ya entries zote
    cur.execute("SELECT COUNT(*) FROM lexicon")
    total_entries = cur.fetchone()[0]

    # 2️⃣ Idadi ya categories tofauti
    cur.execute("SELECT COUNT(DISTINCT category) FROM lexicon")
    distinct_categories = cur.fetchone()[0]

    # 3️⃣ Entries tupu (empty fields)
    cur.execute("""
        SELECT COUNT(*) FROM lexicon
        WHERE english='' OR swahili='' OR category=''
    """)
    empty_entries = cur.fetchone()[0]

    # 4️⃣ Duplicates (maneno yanayojirudia)
    cur.execute("""
        SELECT english, COUNT(*) FROM lexicon
        GROUP BY english HAVING COUNT(*) > 1
    """)
    duplicates = cur.fetchall()

    conn.close()

    # Rudisha data kama dictionary (hii ndiyo muhimu kwa dashboard)
    return {
        "total_entries": total_entries,
        "distinct_categories": distinct_categories,
        "empty_entries": empty_entries,
        "duplicates": duplicates
    }

# Hii inaruhusu script ku-run kama CLI pia
if __name__ == "__main__":
    stats = get_stats()
    print(stats)
