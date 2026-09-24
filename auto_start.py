import os

def run_script(script_name):
    print(f"\n>>> Running {script_name} ...")
    os.system(f"python {script_name}")

def main():
    print("=== MASTER LEXICON AUTO START SYSTEM ===\n")

    # 1️⃣ Kwanza rejesha database ikiwa imeharibika
    run_script("auto_restore.py")

    # 2️⃣ Kisha tengeneza backup mpya
    run_script("auto_backup.py")

    print("\n[✔] Auto start complete — system is ready.")
    print("=== DONE ===")

if __name__ == "__main__":
    main()
