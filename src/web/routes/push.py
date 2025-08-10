from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database.db import SessionLocal
from src.database.models.push_model import PushSubscription

bp = Blueprint("push", __name__, url_prefix="/push")

@bp.route("/subscribe", methods=["POST"])
@jwt_required()
def subscribe():
    user_id = get_jwt_identity()
    data = request.get_json()

    subscription = data.get("subscription")
    if not subscription:
        return jsonify({"error": "Missing 'subscription' data."}), 400

    session = SessionLocal()
    try:
        existing = session.query(PushSubscription).filter_by(user_id=user_id).first()
        if existing:
            existing.subscription_info = subscription
        else:
            new_sub = PushSubscription(user_id=user_id, subscription_info=subscription)
            session.add(new_sub)

        session.commit()
        return jsonify({"msg": "Push subscription updated."}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": f"Subscription failed: {str(e)}"}), 500
    finally:
        session.close()