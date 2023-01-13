import datetime
from shared.database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class UserResponseModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    email = Column(String(30))
    birth_date = Column(String(8))
    password = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=datetime.datetime.now)

    event = relationship("EventModel", back_populates="user")
