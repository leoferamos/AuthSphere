from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.repositories.form_field_repository import FormFieldRepository
from app.core.config.database import get_db

async def get_active_fields(db: AsyncSession = Depends(get_db)):
    """
    Dependency to fetch all active form fields from the database.
    """
    repo = FormFieldRepository(db)
    fields = await repo.get_active_fields()
    return {field.name: field for field in fields}
