from datetime import datetime, timedelta
from typing import List, Dict


def calculate_daily_wellness_score(habits_completed: int, goals_achieved: int, mood_rating: int) -> int:
    """
    Returns a wellness score out of 100 based on user's engagement and mood.
    - habits_completed: Number of habits completed today
    - goals_achieved: Number of goals completed today
    - mood_rating: Mood rating from 1 to 4
    """
    habits_score = min(habits_completed * 10, 30)
    goals_score = min(goals_achieved * 15, 30)
    mood_score = min(max(mood_rating, 1), 4) * 10

    return habits_score + goals_score + mood_score


def calculate_hydration_percentage(current_ml: int, target_ml: int) -> float:
    """
    Returns hydration completion percentage (0–100) based on current and target intake.
    """
    if target_ml == 0:
        return 0.0
    return round((current_ml / target_ml) * 100, 2)


def calculate_focus_duration(task_log: List[Dict[str, str]]) -> int:
    """
    Given a list of task dicts with 'start' and 'end' timestamps (format: HH:MM),
    returns total focused minutes.
    """
    def _parse_time(time_str: str):
        return datetime.strptime(time_str, "%H:%M")

    total_minutes = 0
    for task in task_log:
        try:
            start = _parse_time(task["start"])
            end = _parse_time(task["end"])
            if end < start:
                end += timedelta(days=1)  # handle overnight tasks
            duration = end - start
            total_minutes += duration.total_seconds() / 60
        except (KeyError, ValueError, TypeError):
            continue

    return int(total_minutes)


def summarize_weekly_logs(logs: List[Dict]) -> Dict[str, any]:
    """
    For GPT memory engine: summarize last 7 days of logs.
    Accepts a list of dicts (one per day) with optional keys:
    - 'mood_rating', 'water_ml', 'journaled', 'anxious', 'goals_achieved', 'habits_completed'

    Returns a human-readable summary + structured data.
    """
    days = len(logs)
    mood_sum = water_sum = journal_count = anxious_count = 0
    goal_total = habit_total = 0

    for log in logs:
        mood_sum += log.get("mood_rating", 0)
        water_sum += log.get("water_ml", 0)
        journal_count += int(log.get("journaled", False))
        anxious_count += int(log.get("anxious", False))
        goal_total += log.get("goals_achieved", 0)
        habit_total += log.get("habits_completed", 0)

    summary = {
        "avg_mood": round(mood_sum / days, 2) if days else 0,
        "total_water": water_sum,
        "journaled_days": journal_count,
        "anxious_days": anxious_count,
        "total_goals": goal_total,
        "total_habits": habit_total,
        "text": f"Last week you drank {water_sum}ml water, "
                f"felt anxious {anxious_count} times, "
                f"journaled {journal_count} days, "
                f"completed {goal_total} goals and {habit_total} habits. "
                f"Average mood: {round(mood_sum / days, 1) if days else 'N/A'}."
    }

    return summary