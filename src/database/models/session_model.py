from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from datetime import date
from src.database.db import Base

class SessionLog(Base):
    __tablename__ = "session_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_name = Column(String(100), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    log_date = Column(Date, default=date.today)

    user = relationship("User", back_populates="session_logs")

    def __repr__(self):
        return (
            f"<SessionLog id={self.id} task='{self.task_name}' "
            f"{self.start_time}-{self.end_time} on {self.log_date}>"
        )