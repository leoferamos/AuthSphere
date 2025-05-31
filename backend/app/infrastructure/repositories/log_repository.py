from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.entities.audit_log import AuditLog

class LogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_logs(self):
        result = await self.session.execute(select(AuditLog).order_by(AuditLog.timestamp.desc()))
        return result.scalars().all()

    async def log_action(self, action: str, details: str, user_id: str | None = None):
        new_log = AuditLog(
            action=action,
            details=details,
            user_id=user_id
        )
        self.session.add(new_log)
        await self.session.commit()