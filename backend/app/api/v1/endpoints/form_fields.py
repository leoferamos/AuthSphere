from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config.database import get_db
from app.infrastructure.repositories.form_field_repository import FormFieldRepository

router = APIRouter(tags=["Form Fields"])

@router.get(
    "/form-fields",
    summary="List active registration fields",
    description="Returns the list of active and configurable fields for user registration.",
)
async def list_form_fields(db: AsyncSession = Depends(get_db)):
    repo = FormFieldRepository(db)
    fields = await repo.get_active_fields()
    return [
        {
            "name": field.name,
            "label": field.label,
            "field_type": field.field_type,
            "is_required": field.is_required,
            "is_active": field.is_active,
        }
        for field in fields
    ]