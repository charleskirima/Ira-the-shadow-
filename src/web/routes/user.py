from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date, timedelta
from sqlalchemy import desc
from src.database.db import SessionLocal
from src.database.models import SpiritualLog, User

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    session = SessionLocal()
    try:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "username": user.username,
            "mood": user.mood,
            "belief": user.belief,
            "allow_nudging": user.allow_nudging
        }), 200
    finally:
        session.close()


@bp.route("/update", methods=["POST"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    session = SessionLocal()
    try:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.username = data.get("username", user.username)
        user.mood = data.get("mood", user.mood)
        user.belief = data.get("belief", user.belief)
        session.commit()

        return jsonify({"message": "Profile updated."}), 200
    except Exception as e:
        session.rollback()
        print(f"[❌] Failed to update profile: {e}")
        return jsonify({"error": "Profile update failed."}), 500
    finally:
        session.close()


@bp.route("/spiritual/streak", methods=["GET"])
@jwt_required()
def get_streak():
    user_id = get_jwt_identity()
    session = SessionLocal()
    try:
        logs = session.query(SpiritualLog)\
            .filter_by(user_id=user_id)\
            .order_by(desc(SpiritualLog.log_date))\
            .all()

        if not logs:
            return jsonify({"streak": 0}), 200

        streak = 0
        today = date.today()
        for i, log in enumerate(logs):
            expected_date = today - timedelta(days=i)
            if log.log_date == expected_date:
                streak += 1
            else:
                break

        return jsonify({"streak": streak}), 200
    finally:
        session.close()


@bp.route("/nudging/toggle", methods=["POST"])
@jwt_required()
def toggle_nudging():
    user_id = get_jwt_identity()
    session = SessionLocal()
    try:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.allow_nudging = not user.allow_nudging
        session.commit()
        return jsonify({"nudging_enabled": user.allow_nudging}), 200
    except Exception as e:
        session.rollback()
        print(f"[❌] Failed to toggle nudging: {e}")
        return jsonify({"error": "Toggle failed."}), 500
    finally:
        session.close()