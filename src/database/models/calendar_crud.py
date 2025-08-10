from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.database.models.calendar_model import CalendarEvent

def create_event(db: Session, user_id: int, data: dict) -> CalendarEvent:
    event = CalendarEvent(
        user_id=user_id,
        title=data["title"],
        description=data.get("description"),
        event_type=data.get("event_type", "mental"),
        start_time=data["start_time"],
        end_time=data.get("end_time"),
        is_recurring=data.get("is_recurring", False),
        recurrence_pattern=data.get("recurrence_pattern"),
        reminder_minutes_before=data.get("reminder_minutes_before", 15),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_upcoming_events(db: Session, user_id: int, within_hours: int = 24):
    now = datetime.utcnow()
    future = now + timedelta(hours=within_hours)
    return db.query(CalendarEvent).filter(
        CalendarEvent.user_id == user_id,
        CalendarEvent.start_time >= now,
        CalendarEvent.start_time <= future
    ).all()

def get_event_by_id(db: Session, user_id: int, event_id: int):
    return db.query(CalendarEvent).filter_by(id=event_id, user_id=user_id).first()

def update_event(db: Session, event_id: int, user_id: int, updates: dict):
    event = get_event_by_id(db, user_id, event_id)
    if not event:
        return None
    for key, value in updates.items():
        if hasattr(event, key):
            setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, user_id: int, event_id: int):
    event = get_event_by_id(db, user_id, event_id)
    if event:
        db.delete(event)
        db.commit()
    return event