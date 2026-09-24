import os
import shutil

DB_NAME = "master_lexicon.db"
BACKUP_NAME = "master_lexicon_backup.db"

def main():
    print("=== MASTER LEXICON DATABASE RESTORE TOOL ===\n")

    # 1. Check if backup file exists
    if not os.path.exists(BACKUP_NAME):
        print(f"[X] Backup file '{BACKUP_NAME}' not found!")
        print("    Hakikisha umefanya backup kwanza (python backup_db.py)")
        return

    # 2. Restore backup
    try:
        shutil.copy(BACKUP_NAME, DB_NAME)
        print(f"[✔] Restore complete!")
        print(f"[✔] '{DB_NAME}' imerejeshwa kutoka '{BACKUP_NAME}'")
    except Exception as e:
        print("[X] Restore failed:")
        print(e)
        return

    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
