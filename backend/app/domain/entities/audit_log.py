from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime, timezone
from app.core.config.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True)
    action = Column(String(50), nullable=False)  
    details = Column(Text)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(String(36), nullable=True)  

    def __repr__(self):
        return f"<AuditLog {self.action}>"
