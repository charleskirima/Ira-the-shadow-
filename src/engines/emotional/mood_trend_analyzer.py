# src/engines/emotional/mood_trend_analyzer.py

import datetime
from collections import Counter, defaultdict
from sqlalchemy.orm import Session
from src.business_logic.models import MoodLog, User  # Corrected import

def analyze_user_mood_trends(db: Session):
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    # Get all user IDs with mood logs in the past week
    user_ids = db.query(MoodLog.user_id)\
        .filter(MoodLog.timestamp >= week_ago)\
        .distinct().all()

    for (user_id,) in user_ids:
        logs = db.query(MoodLog).filter(
            MoodLog.user_id == user_id,
            MoodLog.timestamp >= week_ago,
            MoodLog.mood_level != None
        ).all()

        if not logs:
            continue

        mood_counts = Counter()
        mood_by_hour = defaultdict(list)
        mood_levels = []

        for log in logs:
            mood_counts[log.mood_label] += 1
            if log.timestamp:
                hour = log.timestamp.hour
                mood_by_hour[hour].append(log.mood_level)
            mood_levels.append(log.mood_level)

        dominant_mood = mood_counts.most_common(1)[0][0]

        avg_mood_by_hour = {
            hour: sum(levels) / len(levels)
            for hour, levels in mood_by_hour.items()
        }

        best_hour = max(avg_mood_by_hour, key=avg_mood_by_hour.get)
        worst_hour = min(avg_mood_by_hour, key=avg_mood_by_hour.get)

        mean_mood = sum(mood_levels) / len(mood_levels)
        variance = sum((m - mean_mood) ** 2 for m in mood_levels) / len(mood_levels)
        mood_variability = round(variance ** 0.5, 2)

        # Update user profile in User table
        user = db.query(User).filter_by(id=user_id).first()
        if user:
            user.dominant_mood = dominant_mood
            user.best_hour = best_hour
            user.worst_hour = worst_hour
            user.mood_variability_score = mood_variability

    db.commit()
    print("✅ Mood trend analysis complete.")