from typing import List, Dict, Optional, Any

def generate_evening_summary(
    logs: Dict[str, Any],
    goals_completed: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Builds a personalized evening reflection summary.

    Args:
        logs: A dict containing keys like 'mood', 'journal'.
        goals_completed: A list of goals completed today.

    Returns:
        Dict with title, reflections, and optional journal prompt.
    """
    reflections = []

    if goals_completed and len(goals_completed) > 0:
        reflections.append(f"You completed {len(goals_completed)} goals today. 🎯")
    else:
        reflections.append("It's okay if today didn’t go as planned. You still showed up.")

    mood = logs.get("mood", "").strip().lower()
    if mood in ["anxious", "stressed", "tense"]:
        reflections.append("Take a moment to release tension. What’s one thing you can let go of tonight?")
    elif mood:
        reflections.append(f"Your mood was '{mood}'. Reflect on what influenced that feeling.")
    else:
        reflections.append("Reflect on how you felt today.")

    journal_entry = logs.get("journal", "").strip()
    journal_prompt = None
    if not journal_entry:
        journal_prompt = "What are you grateful for today?"

    return {
        "title": "Evening Summary",
        "reflections": reflections,
        "journal_prompt": journal_prompt
    }