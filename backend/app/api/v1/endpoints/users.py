from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserCreate, UserRead
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.utils.security import get_password_hash
from app.core.config.database import get_db
from app.core.dependencies.fields import get_active_fields
from app.core.dependencies.rbac import requires_permission

router = APIRouter(tags=["Users", "Admin"])

@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Supports dynamic fields configured by admin. Check /api/form-fields for available fields."
)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    active_fields: dict = Depends(get_active_fields)
):
    errors = {}
    for field_name, field_config in active_fields.items():
        value = getattr(user_in, field_name, None)
        if field_config.is_required and not value:
            errors[field_name] = f"{field_config.label} is required"
    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"errors": errors}
        )

    user_repo = UserRepository(db)
    if await user_repo.get_by_username(user_in.username):
        raise HTTPException(status_code=409, detail="Username already registered")

    hashed_password = get_password_hash(user_in.password)
    user = await user_repo.create_user(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password
    )
    return user

@router.delete(
    "/users/{user_id}",
    dependencies=[Depends(requires_permission("user:delete"))],
    summary="Delete a user",
    responses={
        403: {"description": "Insufficient permissions"},
        204: {"description": "User deleted"}
    }
)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user_repo.delete(user_id)
    return {"detail": "User deleted"}
