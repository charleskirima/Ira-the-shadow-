from datetime import datetime
from typing import Dict, List, Union

def get_time() -> str:
    """Returns the current UTC timestamp in ISO format."""
    return datetime.utcnow().isoformat()

def log_physical_input(
    user_id: int, 
    sleep_hours: float, 
    water_intake: float, 
    workout_done: bool
) -> Dict[str, Union[int, float, bool, str]]:
    """
    Logs physical health data.
    """
    return {
        "user_id": user_id,
        "sleep": round(sleep_hours, 1),
        "water": round(water_intake, 2),
        "workout": workout_done,
        "timestamp": get_time()
    }

def assess_fitness_health(log: Dict[str, Union[int, float, bool, str]]) -> List[str]:
    """
    Analyzes physical log for potential health issues.
    """
    issues = []
    sleep = float(log.get("sleep", 0))
    water = float(log.get("water", 0))
    workout = bool(log.get("workout", False))

    if sleep < 6.0:
        issues.append("Lack of sleep (recommended 7–9 hrs)")
    if water < 1.5:
        issues.append("Low hydration (aim for 2L+)")
    if not workout:
        issues.append("No workout logged (try light movement)")

    return issues