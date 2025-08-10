from sqlalchemy import Column, Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import date
from src.database.db import Base

class SpiritualLog(Base):
    __tablename__ = "spiritual_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    log_date = Column(Date, default=date.today, nullable=False)

    user = relationship("User", back_populates="spiritual_logs")

    __table_args__ = (
        UniqueConstraint('user_id', 'log_date', name='_user_date_uc'),
    )

    def __repr__(self):
        return f"<SpiritualLog id={self.id} user_id={self.user_id} date={self.log_date}>"