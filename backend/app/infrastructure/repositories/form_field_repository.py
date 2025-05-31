from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.entities.form_field import FormField

class FormFieldRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_fields(self):
        result = await self.session.execute(select(FormField).where(FormField.is_active == True))
        return result.scalars().all()
