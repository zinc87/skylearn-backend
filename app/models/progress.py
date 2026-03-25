from app import db
from datetime import datetime

class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    lesson_id = db.Column(db.String(36), db.ForeignKey("lessons.id"), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("user_id", "lesson_id"),)


class XpHistory(db.Model):
    __tablename__ = "xp_history"

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(255), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
