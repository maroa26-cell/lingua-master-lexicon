import os
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, jsonify
)
from flask_migrate import Migrate
from models import db, Word

# -----------------------------
# CONFIG – RAILWAY COMPATIBLE
# -----------------------------

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DEBUG = os.environ.get("DEBUG", "False") == "True"

    # Railway hutupa DATABASE_URL moja kwa moja (PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///master_lexicon.db"  # fallback local
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


# -----------------------------
# HELPERS
# -----------------------------

def paginate_query(query, page, per_page=50):
    return query.paginate(page=page, per_page=per_page, error_out=False)


# -----------------------------
# PUBLIC ROUTES
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/lexicon")
def lexicon_view():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("q", "", type=str).strip()

    base_query = Word.query

    if search:
        like = f"%{search}%"
        base_query = base_query.filter(
            (Word.english.ilike(like)) |
            (Word.swahili.ilike(like)) |
            (Word.dialect.ilike(like))
        )

    base_query = base_query.order_by(Word.english.asc())
    pagination = paginate_query(base_query, page)

    return render_template(
        "lexicon_view.html",
        words=pagination.items,
        pagination=pagination,
        search=search
    )


# -----------------------------
# ADMIN ROUTES (CRUD)
# -----------------------------

@app.route("/admin")
def admin_dashboard():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("q", "", type=str).strip()

    base_query = Word.query

    if search:
        like = f"%{search}%"
        base_query = base_query.filter(
            (Word.english.ilike(like)) |
            (Word.swahili.ilike(like)) |
            (Word.dialect.ilike(like))
        )

    base_query = base_query.order_by(Word.created_at.desc())
    pagination = paginate_query(base_query, page)

    return render_template(
        "lexicon_admin.html",
        words=pagination.items,
        pagination=pagination,
        search=search
    )


@app.route("/admin/add", methods=["POST"])
def admin_add_word():
    english = request.form.get("english")
    swahili = request.form.get("swahili")
    dialect = request.form.get("dialect")
    notes = request.form.get("notes")

    if not english or not swahili:
        flash("English and Swahili are required.", "error")
        return redirect(url_for("admin_dashboard"))

    new_word = Word(
        english=english.strip(),
        swahili=swahili.strip(),
        dialect=(dialect or "").strip() or None,
        notes=(notes or "").strip() or None
    )

    db.session.add(new_word)
    db.session.commit()

    flash("Word added successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/edit/<int:id>", methods=["GET"])
def admin_edit_form(id):
    word = Word.query.get_or_404(id)
    return render_template("lexicon_edit.html", word=word)


@app.route("/admin/edit/<int:id>", methods=["POST"])
def admin_edit_word(id):
    word = Word.query.get_or_404(id)

    english = request.form.get("english")
    swahili = request.form.get("swahili")
    dialect = request.form.get("dialect")
    notes = request.form.get("notes")

    if not english or not swahili:
        flash("English and Swahili are required.", "error")
        return redirect(url_for("admin_edit_form", id=id))

    word.english = english.strip()
    word.swahili = swahili.strip()
    word.dialect = (dialect or "").strip() or None
    word.notes = (notes or "").strip() or None

    db.session.commit()

    flash("Word updated successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete/<int:id>", methods=["POST"])
def admin_delete_word(id):
    word = Word.query.get_or_404(id)
    db.session.delete(word)
    db.session.commit()
    flash("Word deleted.", "success")
    return redirect(url_for("admin_dashboard"))


# -----------------------------
# API ROUTES
# -----------------------------

@app.route("/admin/api/words")
def admin_api_words():
    search = request.args.get("q", "", type=str).strip()
    base_query = Word.query

    if search:
        like = f"%{search}%"
        base_query = base_query.filter(
            (Word.english.ilike(like)) |
            (Word.swahili.ilike(like)) |
            (Word.dialect.ilike(like))
        )

    words = base_query.order_by(Word.english.asc()).all()
    data = [w.to_dict() for w in words]
    return jsonify({"status": "ok", "count": len(data), "data": data})


# -----------------------------
# ERROR HANDLERS
# -----------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("errors/500.html"), 500


# -----------------------------
# RAILWAY / GUNICORN ENTRYPOINT
# -----------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("PORT", 5001)))
    app.run(host="0.0.0.0", port=port)
