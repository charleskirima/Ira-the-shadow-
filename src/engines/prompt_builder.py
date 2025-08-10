from src.reports.report_utils import score_daily_alignment
from src.database.models.log_models import MoodLog, WaterLog, SleepLog, GoalLog
from datetime import datetime, timedelta
from typing import List, Union

def summarize_list(data: List[Union[str, float]], mode: str = "text") -> Union[str, float]:
    """
    Summarizes a list into either text or numeric format.

    - "text": returns comma-separated unique values
    - "numeric": returns average rounded to 1 decimal
    """
    if not data:
        return "No data" if mode == "text" else 0.0

    if mode == "text":
        return ", ".join(sorted(set(data)))
    if mode == "numeric":
        return round(sum(data) / len(data), 1)

    return "Invalid mode"

def build_system_prompt(user, session) -> str:
    """
    Constructs a GPT system prompt from the user's past week logs.
    """
    today = datetime.now().date()
    last_week = today - timedelta(days=7)

    # Fetch logs
    mood_logs = session.query(MoodLog).filter(
        MoodLog.user_id == user.id,
        MoodLog.timestamp >= last_week
    ).all()
    water_logs = session.query(WaterLog).filter(
        WaterLog.user_id == user.id,
        WaterLog.timestamp >= last_week
    ).all()
    sleep_logs = session.query(SleepLog).filter(
        SleepLog.user_id == user.id,
        SleepLog.timestamp >= last_week
    ).all()
    goals = session.query(GoalLog).filter(
        GoalLog.user_id == user.id,
        GoalLog.timestamp >= last_week,
        GoalLog.completed == True
    ).all()

    # Extract values
    moods = [log.mood for log in mood_logs]
    water = [log.amount for log in water_logs]
    sleep = [log.hours for log in sleep_logs]

    # Calculate alignment
    alignment_score = score_daily_alignment(
        sleep=summarize_list(sleep, "numeric"),
        water=summarize_list(water, "numeric"),
        goals_done=goals
    )

    # Construct final system prompt
    return f"""
You are IRA, the user's co-pilot. Use this weekly memory to guide your advice:
- Mood trend: {summarize_list(moods, "text")}
- Avg Water: {summarize_list(water, "numeric")} L
- Avg Sleep: {summarize_list(sleep, "numeric")} hrs
- Goals Completed: {len(goals)}
- Daily Alignment Score: {alignment_score}/100

Always respond with empathy and specific nudges to improve these scores.
""".strip()