from datetime import datetime
from typing import List, Dict, Tuple

def get_current_time() -> str:
    """Returns the current UTC time in ISO 8601 format."""
    return datetime.utcnow().isoformat()

def log_emotion(user_id: int, emotion: str, note: str = "") -> Dict:
    """
    Creates a structured emotional log entry.

    Args:
        user_id (int): ID of the user.
        emotion (str): Emotional label (e.g., "happy", "anxious").
        note (str, optional): Additional note. Defaults to "".

    Returns:
        Dict: A structured emotional log entry.
    """
    return {
        "user_id": user_id,
        "emotion": emotion,
        "note": note,
        "timestamp": get_current_time()
    }

def detect_emotional_pattern(logs: List[Dict]) -> List[Tuple[str, int]]:
    """
    Analyzes a list of emotional logs and counts emotion frequencies.

    Args:
        logs (List[Dict]): List of emotional log entries.

    Returns:
        List[Tuple[str, int]]: Sorted list of (emotion, frequency) tuples.
    """
    emotion_counts = {}
    for log in logs:
        emotion = log.get("emotion", "neutral")
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

    return sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)