from app import db
from datetime import datetime, date

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True)           # Cognito 'sub' UUID
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    xp = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    last_active = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
