from sqlalchemy import Column, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from src.database.db import Base

class HydrationLog(Base):
    __tablename__ = "hydration_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sleep_hours = Column(Float, nullable=False)
    water_intake = Column(Float, nullable=False)
    log_date = Column(Date, default=date.today)

    user = relationship("User", back_populates="hydration_logs")

    def __repr__(self):
        return (
            f"<HydrationLog id={self.id} user_id={self.user_id} "
            f"sleep={self.sleep_hours}h water={self.water_intake}L date={self.log_date}>"
        )


class SleepLog(Base):
    __tablename__ = "sleep_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hours = Column(Float, nullable=False)
    # Safer version
log_date = Column(Date, default=lambda: date.today())

    user = relationship("User", back_populates="sleep_logs")

    def __repr__(self):
        return (
            f"<SleepLog id={self.id} user_id={self.user_id} "
            f"hours={self.hours}h date={self.log_date}>"
        )