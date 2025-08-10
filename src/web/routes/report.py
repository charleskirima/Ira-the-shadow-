from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

from src.reports import morning_report, midday_checkin, evening_summary
from src.database.db import SessionLocal
from src.database.models import MoodLog, JournalEntry, HydrationLog, Goal

bp = Blueprint("report", __name__, url_prefix="/report")


@bp.route("/morning", methods=["GET"])
@jwt_required()
def morning():
    user_id = get_jwt_identity()
    session = SessionLocal()
    try:
        mood = session.query(MoodLog).filter_by(user_id=user_id, log_date=date.today()).first()
        water = session.query(HydrationLog).filter_by(user_id=user_id, log_date=date.today()).first()

        logs = {
            "sleep_hours": 6.0,  # Replace with real sleep data if available
            "mood": mood.emotion if mood else "unknown",
            "water_intake": water.water_intake if water else 0.0
        }

        return jsonify(morning_report.generate_morning_report(logs))
    except Exception as e:
        print(f"[❌] Morning report error: {e}")
        return jsonify({"error": "Failed to generate morning report."}), 500
    finally:
        session.close()


@bp.route("/midday", methods=["GET"])
@jwt_required()
def midday():
    try:
        # Replace with real-time data or logs in future
        logs = {
            "steps": 1500,
            "energy": "medium",
            "mood": "calm"
        }
        return jsonify(midday_checkin.generate_midday_checkin(logs))
    except Exception as e:
        print(f"[❌] Midday check-in error: {e}")
        return jsonify({"error": "Failed to generate midday check-in."}), 500


@bp.route("/evening", methods=["GET"])
@jwt_required()
def evening():
    user_id = get_jwt_identity()
    session = SessionLocal()
    try:
        mood = session.query(MoodLog).filter_by(user_id=user_id, log_date=date.today()).first()
        journal = session.query(JournalEntry).filter_by(user_id=user_id, log_date=date.today()).first()
        goals = session.query(Goal).filter_by(user_id=user_id).all()

        logs = {
            "mood": mood.emotion if mood else "unknown",
            "journal": journal.content if journal else ""
        }

        formatted_goals = [{"title": g.title} for g in goals]

        return jsonify(evening_summary.generate_evening_summary(logs, formatted_goals))
    except Exception as e:
        print(f"[❌] Evening report error: {e}")
        return jsonify({"error": "Failed to generate evening summary."}), 500
    finally:
        session.close()