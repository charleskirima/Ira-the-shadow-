from typing import List, Dict, Any

def suggest_health_nudges(logs: Dict[str, Any], debug: bool = False) -> List[Dict[str, str]]:
    """
    Suggests contextual health nudges based on daily logs.
    Returns a list of structured nudge dicts: { type, message }

    Types: 'hydration', 'activity'
    """
    nudges: List[Dict[str, str]] = []

    # --- Hydration ---
    try:
        water = float(logs.get("water", 0))
    except (TypeError, ValueError):
        water = 0.0

    if water < 1.0:
        nudges.append({
            "type": "hydration",
            "message": "You're under 1L today. Time for a glass of water!"
        })

    # --- Activity ---
    try:
        steps = int(logs.get("steps", 0))
    except (TypeError, ValueError):
        steps = 0

    if steps < 3000:
        nudges.append({
            "type": "activity",
            "message": "Low activity detected. Try a 5-minute walk break."
        })

    if debug:
        print(f"[DEBUG] Health log input: {logs}")
        print(f"[DEBUG] Generated nudges: {nudges}")

    return nudges