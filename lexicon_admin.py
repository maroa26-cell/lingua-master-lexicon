from flask import Flask, render_template, request, jsonify
import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

# ---------------------------------------------------------
#  GLOBAL CONFIGURATION
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "lingua-master-lexicon.csv")

FIELDNAMES = ["English", "Swahili", "Category"]


# ---------------------------------------------------------
#  HOME ROUTE (Railway Root Fix)
# ---------------------------------------------------------
@app.route("/")
def home():
    return render_template("lexicon_admin.html")


# ---------------------------------------------------------
#  READ ALL ENTRIES (Enterprise Optimized)
# ---------------------------------------------------------
@app.route("/entries", methods=["GET"])
def get_entries():
    if not os.path.exists(CSV_FILE):
        return jsonify([])

    entries = []
    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            entries.append({
                "English": row.get("English", "").strip(),
                "Swahili": row.get("Swahili", "").strip(),
                "Category": row.get("Category", "").strip()
            })

    return jsonify(entries)


# ---------------------------------------------------------
#  ADD NEW ENTRY (Enterprise Validation)
# ---------------------------------------------------------
@app.route("/add", methods=["POST"])
def add_entry():
    data = request.json

    # Validation
    if not data or not data.get("English") or not data.get("Swahili"):
        return jsonify({"error": "Invalid entry"}), 400

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow({
            "English": data["English"].strip(),
            "Swahili": data["Swahili"].strip(),
            "Category": data.get("Category", "").strip()
        })

    return jsonify({"message": "Entry added successfully"})


# ---------------------------------------------------------
#  DELETE ENTRY (Enterprise Safe Delete)
# ---------------------------------------------------------
@app.route("/delete", methods=["POST"])
def delete_entry():
    target = request.json.get("English")
    if not target:
        return jsonify({"error": "Missing English field"}), 400

    rows = []
    found = False

    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["English"] != target:
                rows.append(row)
            else:
                found = True

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    if not found:
        return jsonify({"message": "Entry not found"}), 404

    return jsonify({"message": "Entry deleted"})


# ---------------------------------------------------------
#  UPDATE ENTRY (Enterprise Replace Logic)
# ---------------------------------------------------------
@app.route("/update", methods=["POST"])
def update_entry():
    old_word = request.json.get("old_English")
    new_data = request.json.get("new_data")

    if not old_word or not new_data:
        return jsonify({"error": "Invalid update request"}), 400

    rows = []
    updated = False

    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["English"] == old_word:
                rows.append({
                    "English": new_data.get("English", "").strip(),
                    "Swahili": new_data.get("Swahili", "").strip(),
                    "Category": new_data.get("Category", "").strip()
                })
                updated = True
            else:
                rows.append(row)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    if not updated:
        return jsonify({"message": "Entry not found"}), 404

    return jsonify({"message": "Entry updated"})


# ---------------------------------------------------------
#  EXPORT PDF (Enterprise Pagination)
# ---------------------------------------------------------
@app.route("/export/pdf", methods=["GET"])
def export_pdf():
    pdf_path = os.path.join(BASE_DIR, "MasterLexiconExport.pdf")
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Master Lexicon Export")
    y -= 40

    c.setFont("Helvetica", 11)

    with open(CSV_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            line = f"{row['English']} - {row['Swahili']} ({row['Category']})"
            c.drawString(50, y, line)
            y -= 18

            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 50

    c.save()
    return jsonify({"message": "PDF exported", "file": "MasterLexiconExport.pdf"})


# ---------------------------------------------------------
#  EXPORT CSV
# ---------------------------------------------------------
@app.route("/export/csv", methods=["GET"])
def export_csv():
    return jsonify({"message": "CSV export ready", "file": "lingua-master-lexicon.csv"})


# ---------------------------------------------------------
#  EXPORT EXCEL (CSV FORMAT)
# ---------------------------------------------------------
@app.route("/export/excel", methods=["GET"])
def export_excel():
    return jsonify({"message": "Excel export ready", "file": "lingua-master-lexicon.csv"})


# ---------------------------------------------------------
#  LOCAL DEVELOPMENT ONLY
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
