from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.entities.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    @asynccontextmanager
    async def get_session(self):
        """Context manager to handle session lifecycle."""
        try:
            yield
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def get_by_username(self, username: str) -> User | None:
        async with self.get_session():
            result = await self.session.execute(
                select(User).where(User.username == username)
            )
            return result.scalars().first()
