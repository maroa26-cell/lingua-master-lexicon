import csv

with open("lingua-master-lexicon.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    print("Total rows:", len(rows))
