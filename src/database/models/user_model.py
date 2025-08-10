from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.database.db import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)

    mood = Column(String(32))
    belief = Column(String(64))
    allow_nudging = Column(Boolean, default=True)

    # 🔒 Subscription/Billing Fields
    is_free_lifetime = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    subscription_id = Column(String(128), nullable=True)
    currency = Column(String(8), default="KES")

    # Relationships
    mood_logs = relationship("MoodLog", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    journal_entries = relationship("JournalEntry", back_populates="user")
    hydration_logs = relationship("HydrationLog", back_populates="user")
    spiritual_logs = relationship("SpiritualLog", back_populates="user")
    session_logs = relationship("SessionLog", back_populates="user")
    push_subscription = relationship("PushSubscription", back_populates="user", uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User id={self.id} username='{self.username}'>"