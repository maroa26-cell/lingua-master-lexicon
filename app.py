# ============================================================
# MASTER LEXICON — SUPER PREMIUM ULTRA ENTERPRISE INTERNATIONAL v4
# ============================================================

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, make_response
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, func
from flask_migrate import Migrate
from dotenv import load_dotenv
import pandas as pd
import csv
import io
import os
from datetime import datetime

# ============================================================
# LOAD ENVIRONMENT VARIABLES (.env)
# ============================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "DEFAULT_ENTERPRISE_KEY")

# ============================================================
# FLASK APP CONFIG
# ============================================================

app = Flask(__name__)
app.secret_key = SECRET_KEY

# DATABASE (SQLite local, PostgreSQL production)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ============================================================
# MODELS
# ============================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin / translator / viewer
    password = db.Column(db.String(120), nullable=False)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(120), nullable=False)
    swahili = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    search_count = db.Column(db.Integer, default=0)
    edit_count = db.Column(db.Integer, default=0)

# ============================================================
# INIT DEFAULT USERS
# ============================================================

def init_default_users():
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", role="admin", password="Admin2026")
        translator = User(username="translator", role="translator", password="Trans2026")
        viewer = User(username="viewer", role="viewer", password="View2026")
        db.session.add(admin)
        db.session.add(translator)
        db.session.add(viewer)
        db.session.commit()

# ============================================================
# AUTH + ROLE DECORATOR
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('password')

        user = User.query.filter_by(username=uname, password=pwd).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f"✅ Logged in as {user.username} ({user.role}).", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("⚠️ Wrong username or password.", "error")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("ℹ️ Logged out.", "info")
    return redirect(url_for('login'))

def require_role(*roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if 'role' not in session:
                return redirect(url_for('login'))
            if session['role'] not in roles:
                flash("⚠️ You do not have permission for this action.", "error")
                return redirect(url_for('dashboard'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator

# ============================================================
# DASHBOARD + SEARCH ENGINE v3
# ============================================================

@app.route('/')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))

    sort_field = request.args.get('sort', 'english')
    direction = request.args.get('dir', 'asc')
    category_filter = request.args.get('category', 'all')
    page = request.args.get('page', 1, type=int)

    query = Word.query

    if category_filter != 'all':
        query = query.filter_by(category=category_filter)

    sort_column = getattr(Word, sort_field, Word.english)

    if direction == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    words = query.paginate(page=page, per_page=10)
    categories = [w.category for w in Word.query.distinct(Word.category)]

    return render_template(
        'dashboard.html',
        words=words,
        categories=categories,
        sort_field=sort_field,
        direction=direction,
        category_filter=category_filter,
        search_query="",
        role=session.get('role')
    )

@app.route('/search')
def search():
    if 'role' not in session:
        return redirect(url_for('login'))

    query_text = request.args.get('q', '').strip()
    sort_field = request.args.get('sort', 'english')
    direction = request.args.get('dir', 'asc')
    category_filter = request.args.get('category', 'all')
    page = request.args.get('page', 1, type=int)

    query = Word.query

    if query_text:
        like = f"%{query_text}%"
        query = query.filter(or_(Word.english.ilike(like),
                                 Word.swahili.ilike(like),
                                 Word.category.ilike(like)))
        for w in query.all():
            w.search_count += 1
        db.session.commit()

    if category_filter != 'all':
        query = query.filter_by(category=category_filter)

    sort_column = getattr(Word, sort_field, Word.english)

    if direction == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    words = query.paginate(page=page, per_page=10)
    categories = [w.category for w in Word.query.distinct(Word.category)]

    return render_template(
        'dashboard.html',
        words=words,
        categories=categories,
        sort_field=sort_field,
        direction=direction,
        category_filter=category_filter,
        search_query=query_text,
        role=session.get('role')
    )

@app.route('/live_search')
def live_search():
    if 'role' not in session:
        return redirect(url_for('login'))

    q = request.args.get('q', '').strip()
    results = []

    if q:
        like = f"%{q}%"
        words = Word.query.filter(
            or_(Word.english.ilike(like),
                Word.swahili.ilike(like),
                Word.category.ilike(like))
        ).order_by(Word.search_count.desc()).limit(20).all()

        results = [
            {"id": w.id, "english": w.english, "swahili": w.swahili, "category": w.category}
            for w in words
        ]

    return {"results": results}

@app.route('/suggest')
def suggest():
    if 'role' not in session:
        return redirect(url_for('login'))

    q = request.args.get('q', '').strip()
    suggestions = []
    categories = []
    recent = []

    if q:
        like = f"%{q}%"
        words = Word.query.filter(Word.english.ilike(like)).order_by(Word.search_count.desc()).limit(10).all()
        suggestions = [w.english for w in words]

    cat_counts = db.session.query(Word.category, func.count(Word.id)).group_by(Word.category).order_by(func.count(Word.id).desc()).limit(5).all()
    categories = [c[0] for c in cat_counts]

    recent_words = Word.query.order_by(Word.created_at.desc()).limit(5).all()
    recent = [w.english for w in recent_words]

    return {
        "suggestions": suggestions,
        "categories": categories,
        "recent": recent
    }

# ============================================================
# ADD / EDIT / DELETE
# ============================================================

@app.route('/add_word_page')
@require_role('admin', 'translator')
def add_word_page():
    return render_template('add_word.html', role=session.get('role'))

@app.route('/add_word', methods=['POST'])
@require_role('admin', 'translator')
def add_word():
    english = request.form.get('english')
    swahili = request.form.get('swahili')
    category = request.form.get('category')

    if not english or not swahili or not category:
        flash("⚠️ Fill all fields.", "error")
        return redirect(url_for('add_word_page'))

    new_word = Word(
        english=english.strip(),
        swahili=swahili.strip(),
        category=category.strip()
    )
    db.session.add(new_word)
    db.session.commit()

    flash("✅ Word added.", "success")
    return redirect(url_for('dashboard'))

@app.route('/edit/<int:id>')
@require_role('admin', 'translator')
def edit_word_page(id):
    word = Word.query.get_or_404(id)
    return render_template('edit_word.html', word=word, role=session.get('role'))

@app.route('/edit_word/<int:id>', methods=['POST'])
@require_role('admin', 'translator')
def edit_word(id):
    word = Word.query.get_or_404(id)
    word.english = request.form.get('english').strip()
    word.swahili = request.form.get('swahili').strip()
    word.category = request.form.get('category').strip()
    word.edit_count += 1
    db.session.commit()
    flash("✅ Word updated.", "success")
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>')
@require_role('admin')
def delete_word(id):
    word = Word.query.get_or_404(id)
    db.session.delete(word)
    db.session.commit()
    flash("🗑️ Word deleted.", "info")
    return redirect(url_for('dashboard'))

# ============================================================
# EXPORT
# ============================================================

@app.route('/export_csv')
@require_role('admin')
def export_csv():
    words = Word.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["English", "Swahili", "Category", "Search Count", "Edit Count"])
    for w in words:
        writer.writerow([w.english, w.swahili, w.category, w.search_count, w.edit_count])
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=lexicon_v4.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@app.route('/export_excel')
@require_role('admin')
def export_excel():
    words = Word.query.all()
    df = pd.DataFrame({
        "English": [w.english for w in words],
        "Swahili": [w.swahili for w in words],
        "Category": [w.category for w in words],
        "Search Count": [w.search_count for w in words],
        "Edit Count": [w.edit_count for w in words]
    })
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Lexicon')
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=lexicon_v4.xlsx"
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return response

# ============================================================
# SETTINGS v3 (THEME + LANGUAGE)
# ============================================================

@app.route('/settings')
@require_role('admin')
def settings():
    current_language = session.get('language', 'Kiswahili')
    current_theme = session.get('theme', 'gold')
    return render_template(
        'settings.html',
        current_language=current_language,
        current_theme=current_theme,
        role=session.get('role')
    )

@app.route('/change_language', methods=['POST'])
@require_role('admin')
def change_language():
    selected_language = request.form.get('language')
    session['language'] = selected_language
    flash(f"✅ Language changed to {selected_language}.", "success")
    return redirect(url_for('settings'))

@app.route('/change_theme', methods=['POST'])
@require_role('admin')
def change_theme():
    selected_theme = request.form.get('theme')
    valid_themes = ['gold', 'blue', 'green', 'silver', 'midnight', 'sunset', 'emerald']

    if selected_theme not in valid_themes:
        flash("⚠️ Invalid theme.", "error")
        return redirect(url_for('settings'))

    session['theme'] = selected_theme
    flash(f"✅ Theme changed to {selected_theme.title()}.", "success")
    return redirect(url_for('settings'))

# ============================================================
# ANALYTICS v3
# ============================================================

@app.route('/analytics')
@require_role('admin', 'translator', 'viewer')
def analytics():
    words = Word.query.all()

    category_counts = {}
    for w in words:
        category_counts[w.category] = category_counts.get(w.category, 0) + 1

    labels = list(category_counts.keys())
    values = list(category_counts.values())

    date_counts = db.session.query(
        func.date(Word.created_at),
        func.count(Word.id)
    ).group_by(func.date(Word.created_at)).order_by(func.date(Word.created_at)).all()

    date_labels = [str(d[0]) for d in date_counts]
    date_values = [d[1] for d in date_counts]

    top_searched = Word.query.order_by(Word.search_count.desc()).limit(10).all()
    top_edited = Word.query.order_by(Word.edit_count.desc()).limit(10).all()

    return render_template(
        'analytics.html',
        labels=labels,
        values=values,
        date_labels=date_labels,
        date_values=date_values,
        top_searched=top_searched,
        top_edited=top_edited,
        role=session.get('role')
    )

# ============================================================
# RUN
# ============================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_default_users()
    app.run(debug=True)
