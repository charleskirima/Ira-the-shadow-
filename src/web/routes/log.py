from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from src.database.db import SessionLocal
from src.database.models import MoodLog, JournalEntry, HydrationLog, SpiritualLog
# from src.database.models.sleep_model import SleepLog  # Uncomment when SleepLog is available

bp = Blueprint("log", __name__, url_prefix="/log")

# === Mood Log ===
@bp.route("/mood", methods=["POST"])
@jwt_required()
def log_mood():
    user_id = get_jwt_identity()
    mood = request.json.get("mood")

    if not mood:
        return jsonify({"error": "Mood is required."}), 400

    session = SessionLocal()
    try:
        log = MoodLog(user_id=user_id, emotion=mood, log_date=date.today())
        session.add(log)
        session.commit()
        return jsonify({"message": "Mood logged successfully."}), 201
    finally:
        session.close()


# === Journal Log ===
@bp.route("/journal", methods=["POST"])
@jwt_required()
def log_journal():
    user_id = get_jwt_identity()
    entry = request.json.get("entry")

    if not entry:
        return jsonify({"error": "Journal entry is required."}), 400

    session = SessionLocal()
    try:
        journal = JournalEntry(user_id=user_id, content=entry)
        session.add(journal)
        session.commit()
        return jsonify({"message": "Journal entry saved."}), 201
    finally:
        session.close()


# === Hydration Log ===
@bp.route("/hydration", methods=["POST"])
@jwt_required()
def log_water():
    user_id = get_jwt_identity()
    amount = request.json.get("amount")

    if amount is None:
        return jsonify({"error": "Hydration amount is required."}), 400

    session = SessionLocal()
    try:
        hydration = HydrationLog(user_id=user_id, water_intake=amount)
        session.add(hydration)
        session.commit()
        return jsonify({"message": "Hydration updated."}), 201
    finally:
        session.close()


# === Spiritual Log ===
@bp.route("/spiritual", methods=["POST"])
@jwt_required()
def log_spiritual():
    user_id = get_jwt_identity()
    session = SessionLocal()
    try:
        existing = session.query(SpiritualLog).filter_by(user_id=user_id, log_date=date.today()).first()
        if existing:
            return jsonify({"message": "Already logged today."}), 200

        log = SpiritualLog(user_id=user_id, log_date=date.today())
        session.add(log)
        session.commit()
        return jsonify({"message": "Spiritual practice logged."}), 201
    finally:
        session.close()


# === Financial Log (Temporary Stub) ===
@bp.route("/financial", methods=["POST"])
@jwt_required()
def log_financial():
    user_id = get_jwt_identity()
    data = request.json
    income = data.get("income")
    expenses = data.get("expenses")
    goals = data.get("goals")

    if income is None or expenses is None:
        return jsonify({"error": "Income and expenses required."}), 400

    # TODO: Save to DB when model is defined
    print(f"[Financial Log] User {user_id}: income={income}, expenses={expenses}, goals={goals}")
    return jsonify({"message": "Financial data logged."}), 201


# === Mental Clarity Log (Temporary Stub) ===
@bp.route("/mental", methods=["POST"])
@jwt_required()
def log_mental():
    user_id = get_jwt_identity()
    data = request.json
    clarity = data.get("clarity")
    notes = data.get("notes", "")

    if clarity is None or not (0 <= clarity <= 10):
        return jsonify({"error": "Clarity level must be between 0 and 10."}), 400

    # TODO: Save to DB when model is defined
    print(f"[Mental Log] User {user_id}: clarity={clarity}, notes={notes}")
    return jsonify({"message": "Mental state logged."}), 201


# === Sleep Log (Optional: Only if SleepLog is available) ===
# @bp.route("/sleep", methods=["POST"])
# @jwt_required()
# def log_sleep():
#     user_id = get_jwt_identity()
#     hours = request.json.get("hours")
#
#     if hours is None or hours < 0 or hours > 24:
#         return jsonify({"error": "Invalid sleep hours."}), 400
#
#     session = SessionLocal()
#     try:
#         existing = session.query(SleepLog).filter_by(user_id=user_id, log_date=date.today()).first()
#         if existing:
#             existing.hours = hours
#         else:
#             log = SleepLog(user_id=user_id, hours=hours, log_date=date.today())
#             session.add(log)
#         session.commit()
#         return jsonify({"message": "Sleep logged successfully."}), 201
#     finally:
#         session.close()