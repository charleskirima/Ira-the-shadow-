from src.database.db import SessionLocal
from src.database.models.user_model import User
from src.business_logic.nudge_engine import generate_nudges

def run_daily_tasks():
    print("Running daily routines...")
    # TODO: Add logic for automated reports, daily log rotation, backups, etc.
    print("✔ Daily routines complete.")

def run_nudge_check():
    print("Checking nudges for all users...")
    session = SessionLocal()
    try:
        users = session.query(User).filter_by(allow_nudging=True).all()
        for user in users:
            nudges = generate_nudges(user.id, session)
            for nudge in nudges:
                print(f"[{user.username}] → {nudge}")
                # TODO: Save nudge to DB or send push notification
    except Exception as e:
        print(f"[❌] Error during nudge check: {type(e).__name__} - {e}")
    finally:
        session.close()
    print("✔ Nudge check complete.")

if __name__ == "__main__":
    run_daily_tasks()
    run_nudge_check()