from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.engines.chat_orchestrator import orchestrate_response
from src.business_logic.chat_context import get_user_logs_safe
from src import limiter

bp = Blueprint("chat", __name__, url_prefix="/chat")

@bp.route("/respond", methods=["POST"])
@jwt_required()
@limiter.limit("20 per minute")
def chat():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Message is required."}), 400

    message = data["message"]

    # Step 1: Load user context (e.g., logs, preferences)
    try:
        context = get_user_logs_safe(user_id)
    except Exception as e:
        print(f"[WARN] Failed to load context for user {user_id}: {e}")
        context = {}

    # Step 2: Get assistant response
    try:
        reply = orchestrate_response(message, context)
        return jsonify({"response": reply}), 200

    except Exception as e:
        print(f"[ERROR] Response generation failed for user {user_id}: {e}")
        return jsonify({"error": "Internal assistant error"}), 500