from flask import Flask, render_template_string, jsonify
from stats_lexicon import get_stats
import sqlite3
from collections import Counter

app = Flask(__name__)
DB_NAME = "master_lexicon.db"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Master Lexicon Statistics</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; background-color: #121212; color: #eee; text-align: center; }
        h1 { color: #00ffcc; }
        canvas { margin: 30px auto; background-color: #1e1e1e; border-radius: 8px; padding: 10px; }
    </style>
</head>
<body>
    <h1>Master Lexicon Statistics Dashboard</h1>
    <canvas id="categoryChart" width="400" height="200"></canvas>
    <canvas id="duplicateChart" width="400" height="200"></canvas>
    <script>
        fetch('/data').then(res => res.json()).then(data => {

            // Category chart
            const ctx1 = document.getElementById('categoryChart').getContext('2d');
            new Chart(ctx1, {
                type: 'pie',
                data: {
                    labels: data.categories,
                    datasets: [{
                        label: 'Entries per Category',
                        data: data.counts,
                        backgroundColor: ['#00ffcc','#ffcc00','#ff6699','#66ccff','#33ff99','#ff9966']
                    }]
                }
            });

            // Duplicate chart
            const ctx2 = document.getElementById('duplicateChart').getContext('2d');
            new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: ['Unique Words', 'Duplicates'],
                    datasets: [{
                        label: 'Duplicate Analysis',
                        data: [data.unique, data.duplicates],
                        backgroundColor: ['#00ffcc','#ff3366']
                    }]
                }
            });
        });
    </script>
</body>
</html>
"""

def get_category_stats():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT category FROM lexicon")
    rows = cur.fetchall()
    conn.close()

    categories = [r[0] for r in rows]
    counts = Counter(categories)

    return list(counts.keys()), list(counts.values())

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/data")
def data():
    stats = get_stats()
    categories, counts = get_category_stats()

    duplicates = len(stats["duplicates"])
    unique = stats["total_entries"] - duplicates

    return jsonify({
        "categories": categories,
        "counts": counts,
        "unique": unique,
        "duplicates": duplicates
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)
