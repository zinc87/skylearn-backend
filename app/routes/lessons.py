from flask import Blueprint, jsonify, g
from app.middleware.auth import require_auth
from app.models.lesson import Lesson
from app.models.progress import UserProgress
from app.services.xp import award_xp, get_user_xp
from app import db
import uuid

bp = Blueprint("lessons", __name__, url_prefix="/api/lessons")

# A lesson is locked if the previous lesson has not been completed.
# The first lesson (index 0) is always unlocked.
@bp.route("/", methods=["GET"])
@require_auth
def get_all():
    """Return all lessons with completion/lock status for the current user."""
    lessons = Lesson.query.order_by(Lesson.display_order).all()
    completed = {
        p.lesson_id
        for p in UserProgress.query.filter_by(user_id=g.user_id).all()
    }

    result = []
    for i, lesson in enumerate(lessons):
        prev_completed = i == 0 or lessons[i - 1].id in completed
        result.append({
            "id": lesson.id,
            "title": lesson.title,
            "description": lesson.description,
            "difficulty": lesson.difficulty,
            "xpReward": lesson.xp_reward,
            "estimatedMinutes": lesson.estimated_minutes,
            "completed": lesson.id in completed,
            "locked": not prev_completed and lesson.id not in completed,
            "order": lesson.display_order,
            "content": lesson.content,
            "codeTemplate": lesson.code_template,
        })

    return jsonify(result)

@bp.route("/<lesson_id>", methods=["GET"])
@require_auth
def get_by_id(lesson_id):
    """Return a single lesson by ID."""
    lesson = Lesson.query.get_or_404(lesson_id)
    completed = UserProgress.query.filter_by(
        user_id=g.user_id, lesson_id=lesson_id
    ).first() is not None

    return jsonify({
        "id": lesson.id,
        "title": lesson.title,
        "description": lesson.description,
        "difficulty": lesson.difficulty,
        "xpReward": lesson.xp_reward,
        "estimatedMinutes": lesson.estimated_minutes,
        "completed": completed,
        "locked": False,
        "order": lesson.display_order,
        "content": lesson.content,
        "codeTemplate": lesson.code_template,
    })

# Returns 409 if already completed to prevent duplicate XP awards.
# The unique constraint on UserProgress also enforces this at the DB level.
@bp.route("/<lesson_id>/complete", methods=["POST"])
@require_auth
def complete(lesson_id):
    """Mark a lesson as completed and award XP."""
    lesson = Lesson.query.get_or_404(lesson_id)
    existing = UserProgress.query.filter_by(
        user_id=g.user_id, lesson_id=lesson_id
    ).first()

    if existing:
        return jsonify({"error": "Already completed", "xpEarned": 0, "newTotalXp": get_user_xp(g.user_id)}), 409

    progress = UserProgress(id=str(uuid.uuid4()), user_id=g.user_id, lesson_id=lesson_id)
    db.session.add(progress)
    award_xp(g.user_id, lesson.xp_reward, f"Lesson: {lesson.title}")
    db.session.commit()

    return jsonify({"xpEarned": lesson.xp_reward, "newTotalXp": get_user_xp(g.user_id)})
