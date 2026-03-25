from flask import Blueprint, jsonify
from app.middleware.auth import require_auth
from app.models.user import User
from app.services.xp import get_level

bp = Blueprint("leaderboard", __name__, url_prefix="/api/leaderboard")

@bp.route("/", methods=["GET"])
@require_auth
def get_leaderboard():
    """Return all users ranked by XP (highest first)."""
    users = User.query.order_by(User.xp.desc()).all()

    result = []
    for rank, user in enumerate(users, start=1):
        parts = user.username.split()
        if len(parts) >= 2:
            initials = parts[0][0].upper() + parts[1][0].upper()
        else:
            initials = user.username[:2].upper()

        result.append({
            "rank": rank,
            "user": {
                "id": user.id,
                "username": user.username,
                "xp": user.xp,
                "level": get_level(user.xp),
                "streak": user.streak,
                "avatarInitials": initials,
            },
        })

    return jsonify(result)
