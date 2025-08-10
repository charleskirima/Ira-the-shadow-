from datetime import date
import json

from pywebpush import webpush, WebPushException
from typing import List, Dict

from src.database.models import MoodLog, SpiritualLog, HydrationLog
from src.database.models.push_subscription_model import PushSubscription
from config import VAPID_PRIVATE_KEY, VAPID_CLAIMS, MIN_HYDRATION_L


def generate_nudges(user_id: int, session, debug: bool = False) -> List[Dict]:
    """
    Generates context-aware nudges if the user has not logged key data today.
    Returns a list of nudge objects with 'message' and 'type' fields.
    """
    today = date.today()
    nudges = []

    mood = session.query(MoodLog).filter_by(user_id=user_id, log_date=today).first()
    if not mood:
        nudges.append({
            "type": "mood",
            "message": "How are you feeling today? Let’s log a quick mood."
        })

    water = session.query(HydrationLog).filter_by(user_id=user_id, log_date=today).first()
    if not water or (water.amount is not None and water.amount < MIN_HYDRATION_L):
        nudges.append({
            "type": "hydration",
            "message": "Time for a glass of water? Hydration fuels your focus."
        })

    spiritual = session.query(SpiritualLog).filter_by(user_id=user_id, log_date=today).first()
    if not spiritual:
        nudges.append({
            "type": "spiritual",
            "message": "Take a minute to reflect or pray — your spirit matters."
        })

    if debug:
        print(f"[DEBUG] Nudges generated for user {user_id}: {nudges}")

    return nudges


def send_push(user_id: int, message: str, session, debug: bool = False) -> bool:
    """
    Sends a push notification to a subscribed user using their stored subscription.
    Returns True if sent, False if failed.
    """
    sub = session.query(PushSubscription).filter_by(user_id=user_id).first()
    if not sub:
        if debug:
            print(f"[DEBUG] No push subscription found for user {user_id}")
        return False

    try:
        webpush(
            subscription_info=json.loads(sub.subscription_info),
            data=message,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS
        )
        if debug:
            print(f"[DEBUG] Push sent to user {user_id}: {message}")
        return True
    except WebPushException as e:
        print(f"[PushError] User {user_id}: {str(e)}")
        return False