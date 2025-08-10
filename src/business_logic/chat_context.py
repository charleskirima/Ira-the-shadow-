from datetime import date, timedelta
from src.database.db import SessionLocal
from src.database.models import MoodLog, HydrationLog, Goal, JournalEntry


def get_user_logs_safe(user_id: int) -> list[dict]:
    """
    Fetches user logs for the past 7 days from mood, hydration, goals, and journals.
    Returns a list of 7 dictionaries (one per day) for use in summarizer / GPT memory engine.
    """

    session = SessionLocal()
    try:
        today = date.today()
        week_ago = today - timedelta(days=6)

        # Fetch all logs at once
        moods = session.query(MoodLog).filter(
            MoodLog.user_id == user_id,
            MoodLog.log_date >= week_ago
        ).all()

        hydration = session.query(HydrationLog).filter(
            HydrationLog.user_id == user_id,
            HydrationLog.log_date >= week_ago
        ).all()

        goals = session.query(Goal).filter(Goal.user_id == user_id).all()

        journals = session.query(JournalEntry).filter(
            JournalEntry.user_id == user_id,
            JournalEntry.log_date >= week_ago
        ).all()

        # Convert all to {date: {log data}} structure
        daily_logs = {}

        for i in range(7):
            log_date = week_ago + timedelta(days=i)
            daily_logs[log_date.isoformat()] = {
                "log_date": log_date.isoformat(),
                "mood_rating": None,
                "water_ml": 0,
                "journaled": False,
                "anxious": False,
                "goals_achieved": 0,
                "habits_completed": 0  # Placeholder, not yet modeled
            }

        for mood in moods:
            log = daily_logs.get(mood.log_date.isoformat())
            if log:
                log["mood_rating"] = mood.rating
                log["anxious"] = bool(mood.anxious)

        for water in hydration:
            log = daily_logs.get(water.log_date.isoformat())
            if log:
                log["water_ml"] += water.amount_ml

        for journal in journals:
            log = daily_logs.get(journal.log_date.isoformat())
            if log:
                log["journaled"] = True

        # We aggregate goals (assume all achieved within week)
        for goal in goals:
            if goal.achieved:
                # Very rough: equally distribute across week
                for log in daily_logs.values():
                    log["goals_achieved"] += 1 / 7

        return list(daily_logs.values())

    finally:
        session.close()