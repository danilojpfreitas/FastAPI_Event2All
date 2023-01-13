import datetime
from shared.database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class EventModel(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, autoincrement=True)
    place = Column(String(30))
    name = Column(String(30))
    date = Column(String(8))
    managers = Column(String(100))
    invite_number = Column(Integer)
    event_budget = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("UserResponseModel", back_populates="event")
