from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Lexicon(db.Model):
    __tablename__ = 'lexicon'

    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(150), nullable=False, index=True)
    swahili = db.Column(db.String(150), nullable=False, index=True)
    category = db.Column(db.String(80), nullable=True, index=True)

    def __repr__(self):
        return f"<Lexicon {self.english} - {self.swahili} ({self.category})>"
