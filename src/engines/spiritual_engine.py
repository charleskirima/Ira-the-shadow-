from datetime import datetime
from typing import Dict

def get_time() -> str:
    """Returns the current UTC timestamp in ISO format."""
    return datetime.utcnow().isoformat()

def get_reflection_prompt(belief_system: str) -> str:
    """
    Returns a spiritual reflection prompt based on belief system.
    Falls back to a universal prompt if belief is unknown.

    Args:
        belief_system (str): User's declared belief system (e.g., 'christian').

    Returns:
        str: A tailored or generic reflection question.
    """
    prompts = {
        "christian": "What does grace mean to you today?",
        "muslim": "What did you reflect on during prayer?",
        "buddhist": "What truth have you observed today?",
        "atheist": "What value did you uphold today?"
    }
    return prompts.get(belief_system.strip().lower(), "What guided your spirit today?")

def log_spiritual_entry(user_id: int, entry: str, belief_system: str) -> Dict[str, str | int]:
    """
    Creates a spiritual reflection log entry.

    Args:
        user_id (int): Unique user ID.
        entry (str): User's spiritual note or reflection.
        belief_system (str): User's belief system.

    Returns:
        dict: A structured dictionary of the spiritual log.
    """
    return {
        "user_id": user_id,
        "entry": entry,
        "belief_system": belief_system,
        "timestamp": get_time()
    }