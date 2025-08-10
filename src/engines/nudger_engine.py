from src.database.models.calendar_model import CalendarEvent
from src.database.db import SessionLocal
from datetime import datetime, timedelta
import re

def create_nudge_from_text(user_id: int, message: str):
    """
    Parses messages like 'Remind me to pray at 6am every day'
    and creates a recurring daily calendar event.
    """
    session = SessionLocal()
    try:
        match = re.search(r"remind me to (.+?) at (\d+)(am|pm)", message.lower())
        if not match:
            return "[❌] Could not parse reminder. Please use format like 'Remind me to meditate at 7am'."

        activity = match.group(1).strip()
        hour = int(match.group(2))
        meridian = match.group(3)

        # Convert to 24-hour time
        if meridian == "pm" and hour != 12:
            hour += 12
        elif meridian == "am" and hour == 12:
            hour = 0

        now = datetime.now()
        start_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        if start_time < now:
            start_time += timedelta(days=1)

        event = CalendarEvent(
            user_id=user_id,
            title=f"Reminder: {activity}",
            description="Auto-generated nudge",
            event_type="general",
            start_time=start_time,
            end_time=start_time + timedelta(minutes=15),
            is_recurring=True,
            recurrence_pattern="daily",
            reminder_minutes_before=10
        )

        session.add(event)
        session.commit()

        # Format time nicely
        readable_time = start_time.strftime("%I:%M %p").lstrip("0")
        return f"[✅] Nudge to '{activity}' created at {readable_time} daily."

    except Exception as e:
        return f"[❌] Error: {type(e).__name__} - {e}"

    finally:
        session.close()