from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from datetime import datetime

from src.database.db import SessionLocal
from src.database.models import User
from src.reports import morning_report, midday_checkin, evening_summary
from src.push.push_service import send_notification_to_user

scheduler = BackgroundScheduler()
logger = logging.getLogger("IRA-Scheduler")

def morning_job():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        for user in users:
            logs = {
                "sleep_hours": 6.5,
                "mood": "neutral",
                "water_intake": 0.7
            }
            report = morning_report.generate_morning_report(logs)
            send_notification_to_user(user, report["title"], report["summary"])
    except Exception as e:
        logger.error(f"[Morning Job Error] {type(e).__name__}: {e}")
    finally:
        session.close()

def midday_job():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        for user in users:
            logs = {
                "energy": "medium",
                "steps": 2100,
                "mood": "okay"
            }
            report = midday_checkin.generate_midday_checkin(logs)
            send_notification_to_user(user, report["title"], report["message"])
    except Exception as e:
        logger.error(f"[Midday Job Error] {type(e).__name__}: {e}")
    finally:
        session.close()

def evening_job():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        for user in users:
            logs = {
                "mood": "calm",
                "journal": ""
            }
            report = evening_summary.generate_evening_summary(logs)
            message = "\n".join(report["reflections"])
            send_notification_to_user(user, report["title"], message)
    except Exception as e:
        logger.error(f"[Evening Job Error] {type(e).__name__}: {e}")
    finally:
        session.close()

def init_scheduler():
    logger.info("🔁 Initializing IRA Scheduler...")

    scheduler.add_job(morning_job, CronTrigger(hour=6, minute=0), id="morning_report")
    scheduler.add_job(midday_job, CronTrigger(hour=12, minute=0), id="midday_checkin")
    scheduler.add_job(evening_job, CronTrigger(hour=20, minute=0), id="evening_summary")

    scheduler.start()