import os
import shutil

DB_NAME = "master_lexicon.db"
BACKUP_FOLDER = "backups"

def get_latest_backup():
    if not os.path.exists(BACKUP_FOLDER):
        return None
    backups = [f for f in os.listdir(BACKUP_FOLDER) if f.endswith(".db")]
    if not backups:
        return None
    backups.sort(reverse=True)
    return os.path.join(BACKUP_FOLDER, backups[0])

def main():
    print("=== MASTER LEXICON AUTO RESTORE TOOL ===\n")

    if os.path.exists(DB_NAME):
        print(f"✅ Database '{DB_NAME}' ipo tayari — hakuna kinachohitajika kurejeshwa.")
        return

    latest_backup = get_latest_backup()
    if not latest_backup:
        print("⚠️ Hakuna backup iliyopatikana kwenye folder 'backups'.")
        return

    shutil.copy(latest_backup, DB_NAME)
    print(f"[✔] Database '{DB_NAME}' imeundwa upya kutoka backup '{latest_backup}'.")
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
