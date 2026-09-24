from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Word(db.Model):
    __tablename__ = "words"

    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(255), nullable=False, index=True)
    swahili = db.Column(db.String(255), nullable=False, index=True)
    dialect = db.Column(db.String(255), nullable=True, index=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "english": self.english,
            "swahili": self.swahili,
            "dialect": self.dialect,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }
