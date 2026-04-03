from flask import Blueprint, jsonify, g
from app.middleware.auth import require_auth
from app.models.user import User
from app.models.progress import UserProgress, XpHistory
from app.services.xp import get_level
from datetime import date, timedelta
from app import db

bp = Blueprint("progress", __name__, url_prefix="/api/progress")


@bp.route("/", methods=["GET"])
@require_auth
def get_progress():
    """Return the current user's full progress data."""
    user = User.query.get(g.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    completed = [
        p.lesson_id
        for p in UserProgress.query.filter_by(user_id=g.user_id).all()
    ]

    history = [
        {
            "date": h.earned_at.strftime("%Y-%m-%d"),
            "xp": h.xp,
            "source": h.source,
        }
        for h in XpHistory.query.filter_by(user_id=g.user_id)
            .order_by(XpHistory.earned_at).all()
    ]

    # Generate avatar initials from username
    parts = user.username.split()
    if len(parts) >= 2:
        initials = parts[0][0].upper() + parts[1][0].upper()
    else:
        initials = user.username[:2].upper()

    # Streak is incremented only if the user was active exactly yesterday.
    # If they miss a day, streak resets to 1. If already active today, no change.
    today = date.today()
    if user.last_active is None:
        user.streak = 1
        user.last_active = today
    elif user.last_active == today:
        pass  # already logged in today, no change
    elif user.last_active == today - timedelta(days=1):
        user.streak += 1
        user.last_active = today
    else:
        # missed a day, reset streak
        user.streak = 1
        user.last_active = today
    db.session.commit()

    return jsonify({
        "userId": user.id,
        "username": user.username,
        "email": user.email,
        "xp": user.xp,
        "level": get_level(user.xp),
        "streak": user.streak,
        "avatarInitials": initials,
        "completedLessons": completed,
        "xpHistory": history,
    })
