from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Log(Base):
    __tablename__ = "logs"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=True)
    details = Column(String(1024), nullable=True)