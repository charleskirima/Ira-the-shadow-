from flask import Blueprint, request, jsonify
from src.database.db import SessionLocal
from src.database.models.user_model import User

bp = Blueprint("billing_confirm", __name__, url_prefix="/billing")

@bp.route("/confirm", methods=["POST"])
def confirm_payment():
    data = request.get_json()
    if not data:
        return jsonify({"msg": "No data received"}), 400

    try:
        # 🔍 Parse Safaricom response (MPESA STK Push Callback)
        callback = data.get("Body", {}).get("stkCallback", {})
        result_code = callback.get("ResultCode")

        if result_code != 0:
            return jsonify({"msg": "Payment not successful"}), 400

        metadata = callback.get("CallbackMetadata", {}).get("Item", [])
        transaction_id = callback.get("MpesaReceiptNumber")
        phone_number = None
        amount_paid = None

        for item in metadata:
            name = item.get("Name")
            value = item.get("Value")

            if name == "PhoneNumber":
                phone_number = str(value)
            elif name == "Amount":
                amount_paid = float(value)

        if not phone_number or not amount_paid:
            return jsonify({"msg": "Incomplete callback data"}), 400

        # Normalize Kenyan phone number: last 9 digits (e.g. 07xxxxxxxx)
        phone_suffix = phone_number[-9:]

        session = SessionLocal()
        try:
            user = session.query(User).filter(User.username.endswith(phone_suffix)).first()
            if not user:
                print(f"[⚠] No user found for phone ending in {phone_suffix}")
                return jsonify({"msg": "User not found"}), 404

            user.is_premium = True
            user.subscription_id = transaction_id
            session.commit()

            print(f"[✔] Subscription activated for {user.username}")
            return jsonify({"msg": "User subscription updated"}), 200

        finally:
            session.close()

    except Exception as e:
        print("[❌] Payment confirmation error:", e)
        return jsonify({"msg": "Server error"}), 500