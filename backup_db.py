import os
import shutil

DB_NAME = "master_lexicon.db"
BACKUP_NAME = "master_lexicon_backup.db"

def main():
    print("=== MASTER LEXICON DATABASE BACKUP TOOL ===\n")

    # 1. Check if database exists
    if not os.path.exists(DB_NAME):
        print(f"[X] Database '{DB_NAME}' not found!")
        print("    Hakikisha uko ndani ya: C:\\MasterLexicon\\MasterLexicon")
        return

    # 2. Copy database to backup file
    try:
        shutil.copy(DB_NAME, BACKUP_NAME)
        print(f"[✔] Backup complete!")
        print(f"[✔] File saved as '{BACKUP_NAME}'")
    except Exception as e:
        print("[X] Backup failed:")
        print(e)
        return

    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
