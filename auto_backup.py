import sqlite3
import os
import shutil
from datetime import datetime

DB_NAME = "master_lexicon.db"
BACKUP_FOLDER = "backups"

def main():
    print("=== MASTER LEXICON AUTO BACKUP TOOL ===\n")

    if not os.path.exists(DB_NAME):
        print(f"⚠️ Database '{DB_NAME}' haipatikani!")
        return

    # Unda folder la backups kama halipo
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    # Unda jina la faili lenye tarehe na muda
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_FOLDER, backup_name)

    # Nakili database
    shutil.copy(DB_NAME, backup_path)

    print(f"[✔] Backup imehifadhiwa kama '{backup_path}'")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
