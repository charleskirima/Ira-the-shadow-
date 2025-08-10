from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.database.db import Base

class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", back_populates="journal_entries")

    def __repr__(self):
        return f"<JournalEntry id={self.id} user_id={self.user_id}>"