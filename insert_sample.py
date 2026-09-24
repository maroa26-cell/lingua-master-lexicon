import sqlite3
import os

DB_NAME = "master_lexicon.db"

def main():
    print("=== MASTER LEXICON SAMPLE DATA INSERT ===\n")

    if not os.path.exists(DB_NAME):
        print(f"[X] Database '{DB_NAME}' not found!")
        print("    Hakikisha uko ndani ya: C:\\MasterLexicon\\MasterLexicon")
        print("    Kisha run: python create_db.py\n")
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Sample entries
    samples = [
        ("Hello", "Habari", "Greeting"),
        ("Book", "Kitabu", "Object"),
        ("Water", "Maji", "Nature"),
        ("Love", "Upendo", "Emotion"),
        ("Computer", "Kompyuta", "Technology")
    ]

    cur.executemany("INSERT INTO lexicon (english, swahili, category) VALUES (?, ?, ?)", samples)
    conn.commit()
    conn.close()

    print(f"[✔] {len(samples)} sample entries zimeongezwa kwenye database.")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
