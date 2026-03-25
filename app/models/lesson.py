from app import db
from datetime import datetime

class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20), nullable=False)      # beginner, intermediate, advanced
    xp_reward = db.Column(db.Integer, default=50)
    estimated_minutes = db.Column(db.Integer, default=15)
    display_order = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)                                # Markdown lesson content
    code_template = db.Column(db.Text)                          # Starter C++ code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
