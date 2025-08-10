from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Load DB URL from environment or use fallback SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ira.db")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, echo=os.getenv("SQLALCHEMY_ECHO", "False") == "True")
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

def init_db():
    # Ensure all models are registered before table creation
    from src.business_logic.models import (
        user_model,
        mood_model,
        journal_model,
        goal_model,
        log_model,
        session_model,
        spiritual_log_model,
        push_model
    )
    Base.metadata.create_all(bind=engine)
    print("[✅] Database initialized with all tables.")