from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin@localhost:5432/masterlexicon"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Lexicon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(255), nullable=False)
    swahili = db.Column(db.String(255), nullable=False)

@app.route("/add", methods=["POST"])
def add_word():
    data = request.get_json()
    word = Lexicon(english=data["english"], swahili=data["swahili"])
    db.session.add(word)
    db.session.commit()
    return jsonify({"status": "saved"})

@app.route("/all", methods=["GET"])
def get_all():
    words = Lexicon.query.all()
    return jsonify([{"id": w.id, "english": w.english, "swahili": w.swahili} for w in words])

if __name__ == "__main__":
    app.run(debug=True)
