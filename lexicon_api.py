from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

# -----------------------------
# GLOBAL CONFIGURATION
# -----------------------------
DB_NAME = "lingua-master-lexicon.csv"

# -----------------------------
# QUERY FUNCTION
# -----------------------------
def query_csv(word):
    results = []
    with open(DB_NAME, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if word.lower() in row['english'].lower():
                results.append({
                    "English": row['english'],
                    "Swahili": row['swahili'],
                    "Category": row['category']
                })
    return results

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Master Lexicon API (CSV Edition)",
        "endpoints": ["/search?word=<english_word>", "/all"]
    })

# -----------------------------
# SEARCH ROUTE
# -----------------------------
@app.route("/search")
def search_word():
    word = request.args.get("word", "").strip()
    if not word:
        return jsonify({"error": "Please provide a word parameter"}), 400

    results = query_csv(word)
    if not results:
        return jsonify({"message": f"No results found for '{word}'"}), 404

    return jsonify({"results": results})

# -----------------------------
# GET ALL ENTRIES
# -----------------------------
@app.route("/all")
def get_all():
    data = []
    with open(DB_NAME, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                "English": row['english'],
                "Swahili": row['swahili'],
                "Category": row['category']
            })
    return jsonify({"entries": data, "count": len(data)})

# -----------------------------
# HEALTH CHECK ROUTE
# -----------------------------
@app.route("/health")
def health_check():
    return jsonify({"status": "running", "source": DB_NAME})

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
