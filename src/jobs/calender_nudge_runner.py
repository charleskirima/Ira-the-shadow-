from datetime import datetime, timedelta
from src.database.db import SessionLocal
from src.database.models.calendar_model import CalendarEvent

def check_and_trigger_nudges():
    session = SessionLocal()
    try:
        now = datetime.now()
        upcoming_window = now + timedelta(minutes=10)

        events = session.query(CalendarEvent).filter(
            CalendarEvent.start_time <= upcoming_window,
            CalendarEvent.reminded == False
        ).all()

        for event in events:
            # TODO: Replace with push/email/message
            print(f"[🔔] Nudge for User {event.user_id}: {event.title} at {event.start_time.strftime('%H:%M')}")
            event.reminded = True

        session.commit()
    except Exception as e:
        print(f"[❌] Error in nudge runner: {type(e).__name__} - {e}")
        session.rollback()
    finally:
        session.close()