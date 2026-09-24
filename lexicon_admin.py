from flask import Flask, render_template, request, jsonify
import csv
import os
from reportlab.pdfgen import canvas

app = Flask(__name__)

DB_NAME = "lingua-master-lexicon.csv"
FIELDNAMES = ["english", "swahili", "category"]

# ----------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------

def read_csv():
    data = []
    with open(DB_NAME, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def write_csv(data):
    with open(DB_NAME, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)

# ----------------------------------------
# ROUTES
# ----------------------------------------

@app.route("/")
def home():
    return render_template("lexicon_admin.html")

@app.route("/get_entries")
def get_entries():
    data = read_csv()
    return jsonify({"entries": data, "count": len(data)})

@app.route("/add_entry", methods=["POST"])
def add_entry():
    english = request.form.get("english", "").strip()
    swahili = request.form.get("swahili", "").strip()
    category = request.form.get("category", "").strip()

    if not english or not swahili:
        return jsonify({"error": "English and Swahili fields are required"}), 400

    data = read_csv()
    data.append({"english": english, "swahili": swahili, "category": category})
    write_csv(data)

    return jsonify({"message": "Entry added successfully"})

@app.route("/delete_entry", methods=["POST"])
def delete_entry():
    english = request.form.get("english", "").strip()
    data = read_csv()

    new_data = [row for row in data if row["english"].lower() != english.lower()]
    write_csv(new_data)

    return jsonify({"message": f"Deleted entries for '{english}'"})

@app.route("/update_entry", methods=["POST"])
def update_entry():
    english = request.form.get("english", "").strip()
    swahili = request.form.get("swahili", "").strip()
    category = request.form.get("category", "").strip()

    data = read_csv()
    updated = False

    for row in data:
        if row["english"].lower() == english.lower():
            row["swahili"] = swahili
            row["category"] = category
            updated = True

    write_csv(data)

    if updated:
        return jsonify({"message": "Entry updated successfully"})
    else:
        return jsonify({"error": "Word not found"}), 404

@app.route("/export_pdf")
def export_pdf():
    data = read_csv()
    filename = "MasterLexiconExport.pdf"

    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 12)

    y = 800
    c.drawString(50, y, "Master Lexicon Export")
    y -= 30

    for row in data:
        line = f"{row['english']}  -  {row['swahili']}  ({row['category']})"
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 800

    c.save()

    return jsonify({"message": "PDF exported successfully", "file": filename})

# ----------------------------------------
# RUN SERVER
# ----------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5001)
