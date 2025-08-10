from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import date
from src.database.models import User, MoodLog, HydrationLog
from src.database.db import SessionLocal
from src.reports import morning_report
from src import limiter

bp = Blueprint("auth", __name__, url_prefix="/auth")

def validate_fields(data, *required) -> bool:
    return all(field in data and data[field] for field in required)


@bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    data = request.json
    if not validate_fields(data, "username", "password"):
        return jsonify({"msg": "Missing username or password"}), 400

    session = SessionLocal()
    try:
        if session.query(User).filter_by(username=data["username"]).first():
            return jsonify({"msg": "Username already exists"}), 400

        total_users = session.query(User).count()
        is_free = total_users < 200

        user = User(
            username=data["username"],
            mood="neutral",
            belief=data.get("belief", "none"),
            is_free_lifetime=is_free,
            is_premium=is_free
        )
        user.set_password(data["password"])
        session.add(user)
        session.commit()

        return jsonify({"msg": "User created", "free_for_life": is_free}), 201
    finally:
        session.close()


@bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    data = request.json
    if not validate_fields(data, "username", "password"):
        return jsonify({"msg": "Missing username or password"}), 400

    session = SessionLocal()
    try:
        user = session.query(User).filter_by(username=data["username"]).first()
        if not user or not user.check_password(data["password"]):
            return jsonify({"msg": "Invalid credentials"}), 401

        token = create_access_token(identity=user.id)

        # ✅ Generate Morning Report (optional, shown in logs)
        try:
            today = date.today()
            mood = session.query(MoodLog).filter_by(user_id=user.id, log_date=today).first()
            water = session.query(HydrationLog).filter_by(user_id=user.id, log_date=today).first()

            logs = {
                "sleep_hours": 6.0,  # Placeholder, ideally from SleepLog
                "mood": mood.emotion if mood else "unknown",
                "water_intake": water.water_intake if water else 0.0
            }

            report = morning_report.generate_morning_report(logs)
            print(f"[☀️] Morning Report for {user.username}: {report['summary']}")
        except Exception as e:
            print(f"[WARN] Failed to generate morning report: {e}")

        return jsonify(access_token=token), 200
    finally:
        session.close()


@bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    session = SessionLocal()
    try:
        user = session.get(User, user_id)
        return jsonify({
            "username": user.username,
            "belief": user.belief or "none",
            "is_premium": user.is_premium,
            "free_for_life": user.is_free_lifetime
        })
    finally:
        session.close()