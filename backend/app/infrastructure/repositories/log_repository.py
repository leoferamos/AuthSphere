from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.entities.log import Log

class LogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_logs(self):
        result = await self.session.execute(select(Log).order_by(Log.timestamp.desc()))
        return result.scalars().all()

    async def create_log(self, user_id, action, ip_address=None, details=None):
        log = Log(
            user_id=user_id,
            action=action,
            ip_address=ip_address,
            details=details
        )
        self.session.add(log)
        await self.session.commit()