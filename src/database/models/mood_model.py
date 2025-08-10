from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from src.database.db import Base

class MoodLog(Base):
    __tablename__ = "mood_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    emotion = Column(String(32), nullable=False)
    note = Column(String(255))
    log_date = Column(Date, default=date.today)  # Correct: default=date.today (no parentheses)

    user = relationship("User", back_populates="mood_logs")

    def __repr__(self):
        return f"<MoodLog id={self.id} emotion={self.emotion} date={self.log_date}>"