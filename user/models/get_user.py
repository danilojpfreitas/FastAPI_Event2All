from shared.database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, text


class UserResponseModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    email = Column(String(30))
    password = Column(String(20))
#    createdAt = Column(TIMESTAMP, nullable=False, server_default=func.now())
#    createdAt = Column(TIMESTAMP, nullable=False, autoincrement=True)
#    updatedAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
#    updatedAt = Column(DateTime, nullable=False, autoincrement=True)
