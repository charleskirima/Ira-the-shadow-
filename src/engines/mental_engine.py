from datetime import datetime
from typing import Dict, Union

def get_time() -> str:
    """Returns the current UTC timestamp in ISO 8601 format."""
    return datetime.utcnow().isoformat()

def log_mental_state(user_id: int, clarity_level: int, notes: str) -> Dict[str, Union[str, int]]:
    """
    Logs the user's mental clarity state.

    Args:
        user_id (int): Unique identifier of the user.
        clarity_level (int): Clarity rating on a scale from 1 (low) to 10 (high).
        notes (str): Optional context or comment.

    Returns:
        Dict[str, Union[str, int]]: Structured log entry.
    """
    return {
        "user_id": user_id,
        "clarity": clarity_level,
        "notes": notes,
        "timestamp": get_time()
    }

def suggest_mental_exercise(clarity_level: int) -> str:
    """
    Suggests a mental clarity technique based on user's current state.

    Args:
        clarity_level (int): Clarity rating on a scale from 1 to 10.

    Returns:
        str: Contextual suggestion or affirmation.
    """
    if clarity_level <= 3:
        return "Try deep breathing or a short visualization to refocus."
    elif 4 <= clarity_level <= 6:
        return "Take a mindful pause or journal any mental clutter."
    elif 7 <= clarity_level <= 9:
        return "You're in a good headspace. Keep the momentum going!"
    return "Peak clarity! Use this focus to plan, prioritize, or execute."