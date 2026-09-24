import csv
import os

# Njia kamili za faili zote mbili
file1 = "C:\\MasterLexicon\\MasterLexicon\\lingua-master-lexicon.csv"
file2 = "C:\\MasterLexicon\\MasterLexicon\\lingua-master-lexicon.csv"

def read_csv(path):
    if not os.path.exists(path):
        print(f"⚠️ Faili haipatikani: {path}")
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.reader(f))

rows1 = read_csv(file1)
rows2 = read_csv(file2)

print(f"File 1 rows: {len(rows1)}")
print(f"File 2 rows: {len(rows2)}")

# Angalia tofauti za idadi ya mistari
if len(rows1) != len(rows2):
    print("⚠️ Idadi ya mistari inatofautiana kati ya faili hizi mbili.\n")

# Linganisha line kwa line
for i, (r1, r2) in enumerate(zip(rows1, rows2), start=1):
    if r1 != r2:
        print(f"🔍 Tofauti kwenye mstari wa {i}:")
        print("Local Disk:", r1)
        print("Notepad++ :", r2)
        print("-" * 80)

# Ikiwa hakuna tofauti
if rows1 == rows2:
    print("✅ Faili zote mbili zinafanana kabisa.")
