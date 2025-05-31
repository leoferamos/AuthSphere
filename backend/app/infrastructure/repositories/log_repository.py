from sqlalchemy import select
from app.domain.entities.audit_log import AuditLog

class LogRepository:
    def __init__(self, session):
        self.session = session

    async def get_all_logs(self):
        result = await self.session.execute(select(AuditLog).order_by(AuditLog.timestamp.desc()))
        return result.scalars().all()