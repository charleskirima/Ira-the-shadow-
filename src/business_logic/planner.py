from datetime import datetime, timedelta
from typing import List, Dict, Any


def generate_daily_plan(user_goals: List[Dict[str, Any]], sleep_hours: float, mood: str, debug: bool = False) -> List[Dict[str, str]]:
    """
    Generates a structured daily plan based on sleep, mood, and goals.
    Returns a list of plan items, each with 'type' and 'message'.

    Plan item types: 'health', 'focus', 'selfcare'
    """
    plan = []

    if sleep_hours is not None and sleep_hours < 6:
        plan.append({
            "type": "health",
            "message": "You slept less than 6 hours. Consider a 15-minute power nap."
        })

    if mood and mood.lower() in {"stressed", "anxious", "overwhelmed"}:
        plan.append({
            "type": "selfcare",
            "message": "Feeling tense? Try a 5-minute breathing exercise."
        })

    for goal in user_goals or []:
        title = goal.get("title", "Unnamed Task")
        duration = goal.get("duration", 30)

        try:
            duration = int(duration)
        except (ValueError, TypeError):
            duration = 30

        plan.append({
            "type": "focus",
            "message": f"Focus block: {title} for {duration} minutes."
        })

    if debug:
        print(f"[DEBUG] Generated {len(plan)} plan items: {plan}")

    return plan


def suggest_break_times(work_sessions: List[Dict[str, Any]]) -> List[str]:
    """
    Suggests short breaks after each work session ends.
    Each session must have an 'end' datetime object.
    Returns ISO-formatted time strings.
    """
    break_times = []

    for session in work_sessions:
        end_time = session.get("end")
        if isinstance(end_time, datetime):
            break_time = end_time + timedelta(minutes=5)
            break_times.append(break_time.isoformat())

    return break_times