from flask import Flask, render_template_string, jsonify, request, redirect
from stats_lexicon import get_stats
import sqlite3
from collections import Counter
import random
import csv
import os
import json
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
DB_NAME = "master_lexicon.db"

# -------------------------
# SIMPLE JWT-LIKE TOKENS
# -------------------------
USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "viewer": {"password": "viewer123", "role": "viewer"}
}

SESSIONS = {}  # token -> {user, role, exp}

def create_token(user, role):
    token = os.urandom(16).hex()
    SESSIONS[token] = {
        "user": user,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=4)
    }
    return token

def validate_token(token):
    if token not in SESSIONS:
        return None
    data = SESSIONS[token]
    if datetime.now(timezone.utc) > data["exp"]:
        del SESSIONS[token]
        return None
    return data

# -------------------------
# FIXED DECORATOR (NO DUPLICATE ENDPOINTS)
# -------------------------
def login_required(role=None):
    def wrapper(func):
        def inner(*args, **kwargs):
            token = request.args.get("token")
            info = validate_token(token)
            if not info:
                return redirect("/login")
            if role and info["role"] != role:
                return "Access Denied"
            request.user_info = info
            return func(*args, **kwargs)
        inner.__name__ = func.__name__
        return inner
    return wrapper

# -------------------------
# AUDIT LOGS & EVENTS
# -------------------------
LOG_FILE = "lexicon_audit.log"
EVENTS = []  # in-memory events for timeline / notifications

def log_event(event_type, message, user="system"):
    entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "type": event_type,
        "user": user,
        "message": message
    }
    EVENTS.append(entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# -------------------------
# HTML TEMPLATE
# -------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Master Lexicon Control Center v5</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; background-color: #121212; color: #eee; }
        nav { background: #1e1e1e; padding: 15px; text-align: center; }
        nav a { color: #00ffcc; margin: 0 20px; text-decoration: none; font-size: 18px; }
        .tab { display: none; padding: 20px; }
        canvas { margin: 30px auto; background-color: #1e1e1e; border-radius: 8px; padding: 10px; }
        .toggle { position: fixed; top: 20px; right: 20px; cursor: pointer; }
        #timeline, #notifications, #errors { background:#1e1e1e; padding:10px; border-radius:8px; max-height:300px; overflow-y:auto; }
        .item { border-bottom:1px solid #333; padding:5px 0; }
    </style>
    <script>
        function showTab(id) {
            document.querySelectorAll('.tab').forEach(t => t.style.display = 'none');
            document.getElementById(id).style.display = 'block';
        }
        function toggleTheme() {
            let b = document.body;
            if (b.style.backgroundColor === 'white') {
                b.style.backgroundColor = '#121212';
                b.style.color = '#eee';
            } else {
                b.style.backgroundColor = 'white';
                b.style.color = '#000';
            }
        }
        function refreshRealtime() {
            fetch('/realtime?token={{token}}').then(r => r.json()).then(d => {
                let tl = document.getElementById('timeline');
                let nt = document.getElementById('notifications');
                let er = document.getElementById('errors');
                tl.innerHTML = '';
                nt.innerHTML = '';
                er.innerHTML = '';
                d.timeline.forEach(e => {
                    tl.innerHTML += "<div class='item'><b>"+e.time+"</b> ["+e.type+"] "+e.user+": "+e.message+"</div>";
                });
                d.notifications.forEach(e => {
                    nt.innerHTML += "<div class='item'><b>"+e.time+"</b> "+e.message+"</div>";
                });
                d.errors.forEach(e => {
                    er.innerHTML += "<div class='item'><b>"+e.time+"</b> "+e.message+"</div>";
                });
            });
        }
        setInterval(refreshRealtime, 5000);
    </script>
</head>
<body onload="showTab('stats');refreshRealtime();">

<div class="toggle" onclick="toggleTheme()">🌗 Theme</div>

<nav>
    <a href="#" onclick="showTab('stats')">📊 Stats</a>
    <a href="#" onclick="showTab('admin')">🛠️ Admin</a>
    <a href="#" onclick="showTab('api')">🔌 API Tester</a>
    <a href="#" onclick="showTab('health')">❤️ Health</a>
    <a href="#" onclick="showTab('logs')">📜 Logs</a>
    <a href="/export_csv?token={{token}}">📤 Export CSV</a>
</nav>

<div id="stats" class="tab">
    <h1>Statistics Dashboard v5</h1>
    <canvas id="categoryChart"></canvas>
    <canvas id="duplicateChart"></canvas>
    <canvas id="growthChart"></canvas>
    <canvas id="emptyChart"></canvas>
    <canvas id="healthGauge"></canvas>
</div>

<div id="admin" class="tab">
    <h1>Admin Panel</h1>
    <iframe src="http://127.0.0.1:5001" width="100%" height="700" style="border:none;"></iframe>
</div>

<div id="api" class="tab">
    <h1>API Tester</h1>
    <iframe src="http://127.0.0.1:5000" width="100%" height="700" style="border:none;"></iframe>
</div>

<div id="health" class="tab">
    <h1>System Health</h1>
    <iframe src="http://127.0.0.1:5004" width="100%" height="700" style="border:none;"></iframe>
</div>

<div id="logs" class="tab">
    <h1>Activity Timeline & Notifications & Errors</h1>
    <h3>Timeline</h3>
    <div id="timeline"></div>
    <h3>Notifications</h3>
    <div id="notifications"></div>
    <h3>Errors</h3>
    <div id="errors"></div>
</div>

<script>
fetch('/data?token={{token}}').then(r => r.json()).then(d => {

    new Chart(document.getElementById('categoryChart'), {
        type: 'pie',
        data: { labels: d.categories, datasets: [{ data: d.counts }] }
    });

    new Chart(document.getElementById('duplicateChart'), {
        type: 'bar',
        data: { labels: ['Unique','Duplicates'], datasets: [{ data: [d.unique, d.duplicates] }] }
    });

    new Chart(document.getElementById('growthChart'), {
        type: 'line',
        data: { labels: d.growth_labels, datasets: [{ data: d.growth_values }] }
    });

    new Chart(document.getElementById('emptyChart'), {
        type: 'pie',
        data: { labels: ['Filled','Empty'], datasets: [{ data: [d.total_entries - d.empty_entries, d.empty_entries] }] }
    });

    new Chart(document.getElementById('healthGauge'), {
        type: 'doughnut',
        data: { labels: ['Health','Remaining'], datasets: [{ data: [d.health_score, 100 - d.health_score] }] },
        options: { rotation: -90, circumference: 180 }
    });

});
</script>

</body>
</html>
"""

# -------------------------
# CATEGORY STATS
# -------------------------
def get_category_stats():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT category FROM lexicon")
    rows = cur.fetchall()
    conn.close()
    c = Counter([r[0] for r in rows])
    return list(c.keys()), list(c.values())

# -------------------------
# ROUTES (ALL FIXED WITH UNIQUE ENDPOINTS)
# -------------------------

@app.route("/login", methods=["GET", "POST"], endpoint="login_view")
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]
        if user in USERS and USERS[user]["password"] == pwd:
            token = create_token(user, USERS[user]["role"])
            log_event("login", "User logged in", user)
            return redirect(f"/?token={token}")
        log_event("login_failed", "Invalid credentials", user)
        return "Invalid credentials"
    return """
    <form method='POST'>
        <h2>Login</h2>
        Username: <input name='username'><br><br>
        Password: <input name='password' type='password'><br><br>
        <button>Login</button>
    </form>
    """

@app.route("/", endpoint="home_view")
@login_required()
def home():
    token = request.args.get("token")
    log_event("view_dashboard", "Dashboard viewed", request.user_info["user"])
    return render_template_string(HTML, token=token)

@app.route("/data", endpoint="data_view")
@login_required()
def data():
    s = get_stats()
    cats, counts = get_category_stats()
    dup = len(s["duplicates"])
    uniq = s["total_entries"] - dup
    growth_labels = ["Day 1","Day 2","Day 3","Day 4","Day 5"]
    growth_values = [random.randint(1, s["total_entries"]) for _ in growth_labels]
    health = max(0, 100 - (dup * 5 + s["empty_entries"] * 10))

    log_event("stats_fetch", "Stats data fetched", request.user_info["user"])

    return jsonify({
        "categories": cats,
        "counts": counts,
        "unique": uniq,
        "duplicates": dup,
        "growth_labels": growth_labels,
        "growth_values": growth_values,
        "total_entries": s["total_entries"],
        "empty_entries": s["empty_entries"],
        "health_score": health
    })

@app.route("/export_csv", endpoint="export_csv_view")
@login_required("admin")
def export_csv():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT english, swahili, category FROM lexicon")
    rows = cur.fetchall()
    conn.close()

    with open("lexicon_export.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["English", "Swahili", "Category"])
        writer.writerows(rows)

    log_event("export_csv", "CSV exported", request.user_info["user"])
    return "CSV Exported Successfully!"

@app.route("/realtime", endpoint="realtime_view")
@login_required()
def realtime():
    timeline = EVENTS[-30:]
    notifications = [e for e in timeline if e["type"] in ("login","export_csv","stats_fetch","view_dashboard")]
    errors = [e for e in timeline if "error" in e["type"].lower() or "failed" in e["type"].lower()]
    return jsonify({
        "timeline": timeline,
        "notifications": notifications,
        "errors": errors
    })

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    log_event("system_start", "Lexicon v5 dashboard started")
    app.run(debug=True, port=5007)
