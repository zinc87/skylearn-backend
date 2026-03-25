from flask import Blueprint, jsonify, g
from app.middleware.auth import require_auth
from app.models.user import User
from app.models.progress import UserProgress, XpHistory
from app.services.xp import get_level

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
