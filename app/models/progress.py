from app import db
from datetime import datetime

# Tracks which lessons a user has completed. The unique constraint on (user_id, lesson_id)
# prevents duplicate completions and double XP awards.
class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    lesson_id = db.Column(db.String(36), db.ForeignKey("lessons.id"), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("user_id", "lesson_id"),)

# Logs every XP award event for a user. Used to display XP history on the profile page.
class XpHistory(db.Model):
    __tablename__ = "xp_history"

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    xp = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(255), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
