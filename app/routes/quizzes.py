from flask import Blueprint, jsonify, request, g
from app.middleware.auth import require_auth
from app.models.quiz import QuizQuestion, QuizSubmission
from app.services.xp import award_xp, get_user_xp
from app import db
import uuid

bp = Blueprint("quizzes", __name__, url_prefix="/api/quizzes")

@bp.route("/", methods=["GET"])
@require_auth
def get_by_lesson():
    """Return quiz questions for a given lesson."""
    lesson_id = request.args.get("lessonId")
    if not lesson_id:
        return jsonify({"error": "lessonId query parameter is required"}), 400

    questions = QuizQuestion.query.filter_by(lesson_id=lesson_id).all()
    return jsonify([
        {
            "id": q.id,
            "lessonId": q.lesson_id,
            "question": q.question,
            "options": q.options,
            "correctIndex": q.correct_index,
            "explanation": q.explanation,
        }
        for q in questions
    ])

@bp.route("/submit", methods=["POST"])
@require_auth
def submit():
    """Grade quiz answers and award XP."""
    data = request.get_json()
    lesson_id = data.get("lessonId")
    answers = data.get("answers", {})

    if not lesson_id or not answers:
        return jsonify({"error": "lessonId and answers are required"}), 400

    questions = QuizQuestion.query.filter_by(lesson_id=lesson_id).all()
    total = len(questions)
    score = 0

    for q in questions:
        user_answer = answers.get(q.id)
        if user_answer is not None and user_answer == q.correct_index:
            score += 1

    passed = total > 0 and (score / total) >= 0.6

    # Award XP: 10 XP per correct answer, only if not already submitted
    existing = QuizSubmission.query.filter_by(
        user_id=g.user_id, lesson_id=lesson_id
    ).first()

    xp_earned = 0
    
    submission = QuizSubmission(
        id=str(uuid.uuid4()),
        user_id=g.user_id,
        lesson_id=lesson_id,
        score=score,
        total=total,
        xp_earned=xp_earned,
    )
    db.session.add(submission)
    db.session.commit()

    return jsonify({
        "score": score,
        "total": total,
        "xpEarned": xp_earned,
        "newTotalXp": get_user_xp(g.user_id),
        "passed": passed,
    })
