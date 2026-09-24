from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "masterlexicon_secret_key"

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    conn = sqlite3.connect("master_lexicon.db")
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username = ?", (username,))
        user = cur.fetchone()

        if user:
            stored_hash = user["password"]
            import bcrypt
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                session["user"] = username
                return redirect("/")
        
        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")

# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/", methods=["GET"])
def index():
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM lexicon ORDER BY english ASC")
    entries = cur.fetchall()
    conn.close()

    return render_template("index.html", entries=entries)

# -----------------------------
# ADD ENTRY
# -----------------------------
@app.route("/add", methods=["POST"])
def add_entry():
    if "user" not in session:
        return redirect("/login")

    english = request.form.get("english")
    swahili = request.form.get("swahili")
    category = request.form.get("category")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO lexicon (english, swahili, category) VALUES (?, ?, ?)",
        (english, swahili, category)
    )
    conn.commit()
    conn.close()

    return redirect("/")

# -----------------------------
# DELETE ENTRY
# -----------------------------
@app.route("/delete/<int:entry_id>", methods=["POST"])
def delete_entry(entry_id):
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM lexicon WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

    return redirect("/")

# -----------------------------
# SEARCH FUNCTION
# -----------------------------
@app.route("/search", methods=["GET"])
def search():
    if "user" not in session:
        return redirect("/login")

    query = request.args.get("q", "").strip()

    if query == "":
        return redirect("/")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM lexicon
        WHERE english LIKE ? OR swahili LIKE ? OR category LIKE ?
        ORDER BY english ASC
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))

    entries = cur.fetchall()
    conn.close()

    return render_template("index.html", entries=entries)

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
