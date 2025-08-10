from typing import Dict, Any

def generate_midday_checkin(logs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a midday status update and action plan.

    Args:
        logs: A dictionary with:
            - energy: str (e.g., "high", "medium", "low")
            - steps: int
            - mood: str (e.g., "neutral", "stressed")

    Returns:
        Dict with title, message, and suggested actions.
    """
    energy = str(logs.get("energy", "unknown")).strip().lower()
    steps = logs.get("steps", 0)
    try:
        steps = int(steps)
    except (ValueError, TypeError):
        steps = 0

    mood = str(logs.get("mood", "neutral")).strip().lower()

    message = (
        f"Midday check-in:\n"
        f"• Mood: {mood.capitalize()} \n"
        f"• Steps: {steps} \n"
        f"• Energy: {energy.capitalize()}"
    )

    actions = []
    if steps < 3000:
        actions.append("🚶‍♂️ Take a short walk to boost circulation.")
    if energy == "low":
        actions.append("🧘 Stretch or try a 2-minute breathing reset.")
    if mood in ["stressed", "tense", "anxious"]:
        actions.append("📓 Try a calming journal or quick prayer.")

    return {
        "title": "Midday Report",
        "message": message,
        "actions": actions
    }