from flask import Blueprint, jsonify, request
from app.middleware.auth import require_auth
from app.services.judge0 import run_code

bp = Blueprint("code", __name__, url_prefix="/api/code")

@bp.route("/run", methods=["POST"])
@require_auth
def run():
    """Compile and run C++ code via Judge0."""
    data = request.get_json()
    source_code = data.get("sourceCode")
    stdin = data.get("stdin", "")

    if not source_code:
        return jsonify({"error": "sourceCode is required"}), 400

    try:
        result = run_code(source_code, stdin)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Code execution failed: {str(e)}"}), 500
