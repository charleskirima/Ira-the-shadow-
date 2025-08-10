from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database.db import SessionLocal
from src.database.models.session_model import UserSession
from datetime import datetime, timedelta

bp = Blueprint("session", __name__, url_prefix="/session")

@bp.route("/start", methods=["POST"])
@jwt_required()
def start_session():
    user_id = get_jwt_identity()
    device = request.headers.get("User-Agent", "Unknown")[:255]  # Limit length
    ip = request.remote_addr or "0.0.0.0"

    session = SessionLocal()
    try:
        user_session = UserSession(
            user_id=user_id,
            device=device,
            ip_address=ip,
            login_time=datetime.utcnow(),
            last_active=datetime.utcnow(),
            status="active"
        )
        session.add(user_session)
        session.commit()
        return jsonify({"message": "Session started", "session_id": user_session.id}), 201
    except Exception as e:
        session.rollback()
        print(f"[❌] Failed to start session for user {user_id}: {e}")
        return jsonify({"error": "Failed to start session"}), 500
    finally:
        session.close()


@bp.route("/ping", methods=["POST"])
@jwt_required()
def ping():
    user_id = get_jwt_identity()
    session = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(hours=12)  # Optional filter
        latest_session = session.query(UserSession).filter_by(
            user_id=user_id, status="active"
        ).filter(UserSession.login_time >= cutoff)\
         .order_by(UserSession.login_time.desc()).first()

        if latest_session:
            latest_session.last_active = datetime.utcnow()
            session.commit()
            return jsonify({"message": "Activity pinged"}), 200
        else:
            return jsonify({"message": "No active session found"}), 404
    except Exception as e:
        session.rollback()
        print(f"[❌] Failed to ping session for user {user_id}: {e}")
        return jsonify({"error": "Ping failed"}), 500
    finally:
        session.close()


@bp.route("/end", methods=["POST"])
@jwt_required()
def end_session():
    user_id = get_jwt_identity()
    session = SessionLocal()
    try:
        active_sessions = session.query(UserSession).filter_by(
            user_id=user_id, status="active"
        ).all()

        for s in active_sessions:
            s.status = "revoked"
            s.logout_time = datetime.utcnow()  # Requires logout_time field in DB

        session.commit()
        return jsonify({"message": f"{len(active_sessions)} session(s) ended."}), 200
    except Exception as e:
        session.rollback()
        print(f"[❌] Failed to end sessions for user {user_id}: {e}")
        return jsonify({"error": "Failed to end sessions"}), 500
    finally:
        session.close()