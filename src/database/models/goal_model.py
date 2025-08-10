from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.database.db import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", back_populates="goals")

    def __repr__(self):
        return f"<Goal id={self.id} title='{self.title}' duration={self.duration}min>"