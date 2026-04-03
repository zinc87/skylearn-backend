from app import db
from datetime import datetime
import json

# A single quiz question linked to a lesson. options is a JSON array of answer strings.
# correct_index is 0-based and compared against the user's selected answer index.
class QuizQuestion(db.Model):
    __tablename__ = "quiz_questions"

    id = db.Column(db.String(36), primary_key=True)
    lesson_id = db.Column(db.String(36), db.ForeignKey("lessons.id"), nullable=False)
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)                # JSON array of strings
    correct_index = db.Column(db.Integer, nullable=False)
    explanation = db.Column(db.Text)

# Records a user's quiz attempt. Only one submission per user per lesson is used for XP.
class QuizSubmission(db.Model):
    __tablename__ = "quiz_submissions"

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    lesson_id = db.Column(db.String(36), db.ForeignKey("lessons.id"), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    xp_earned = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
