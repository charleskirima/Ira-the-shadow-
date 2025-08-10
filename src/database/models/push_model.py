from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.database.db import Base

class PushSubscription(Base):
    __tablename__ = "push_subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_info = Column(Text, nullable=False)

    user = relationship("User", back_populates="push_subscriptions")

    def __repr__(self):
        return f"<PushSubscription id={self.id} user_id={self.user_id}>"