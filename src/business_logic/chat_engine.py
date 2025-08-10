def interpret_intent(user_message: str) -> str:
    """
    Interprets the user's message to identify intent.
    Returns one of: sleep_advice, emotional_support, daily_planner, nudge_event, or general_query.
    """

    if not isinstance(user_message, str) or not user_message.strip():
        return "general_query"

    lowered = user_message.strip().lower()

    INTENT_RULES = {
        "sleep_advice": ["sleep", "rest", "tired", "insomnia"],
        "emotional_support": ["anxious", "stress", "depressed", "worried", "panic", "overwhelmed"],
        "daily_planner": ["goal", "plan", "schedule", "tasks", "organize"],
        "nudge_event": ["remind", "reminder", "remember to", "note to self"],
    }

    for intent, keywords in INTENT_RULES.items():
        if any(keyword in lowered for keyword in keywords):
            return intent

    return "general_query"


def fallback_response(debug: bool = False) -> str:
    """
    Returns a generic fallback message.
    If debug is True (e.g., investor mode), appends internal tags.
    """
    base_response = (
        "I'm here to support you. Could you share more about your current state or what you'd like to focus on?"
    )
    return f"{base_response} {'[fallback_mode]' if debug else ''}"