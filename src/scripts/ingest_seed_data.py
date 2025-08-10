from src.database.db import SessionLocal
from src.database.models.user_model import User
from sqlalchemy.exc import IntegrityError

def seed_users():
    session = SessionLocal()
    try:
        if session.query(User).filter_by(username="ira_user").first():
            print("User 'ira_user' already exists. Skipping.")
            return

        test_user = User(username="ira_user")
        test_user.set_password("demo123")  # Uses secure hash
        session.add(test_user)
        session.commit()
        print("✅ Seed user 'ira_user' created with password 'demo123' (for dev use only).")

    except IntegrityError:
        print("[❌] Integrity error: user already exists or schema mismatch.")
    except Exception as e:
        print(f"[❌] Failed to seed user: {type(e).__name__} - {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_users()