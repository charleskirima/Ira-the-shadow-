from src.database.db import Base, engine
import sys

def confirm_reset() -> bool:
    """
    Prompts user for confirmation before resetting the database.
    """
    confirmation = input("⚠️  This will DROP and recreate ALL tables. Type 'YES' to continue: ")
    return confirmation == "YES"

def reset_database():
    """
    Drops all tables and recreates them based on current models.
    """
    try:
        print("🧨 Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ Tables dropped.")

        print("🛠 Recreating all tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database reset complete.")
    except Exception as e:
        print(f"[❌] Database reset failed: {type(e).__name__} - {e}")

if __name__ == "__main__":
    if confirm_reset():
        reset_database()
    else:
        print("❌ Operation cancelled.")
        sys.exit()