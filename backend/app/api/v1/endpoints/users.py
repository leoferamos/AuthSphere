from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserCreate, UserRead
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.utils.security import get_password_hash
from app.core.config.database import get_db
from app.core.dependencies.fields import get_active_fields
from app.core.dependencies.rbac import requires_permission
from app.infrastructure.repositories.log_repository import LogRepository

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

@router.patch(
    "/users/{user_id}/roles",
    dependencies=[Depends(requires_permission("user:edit_roles"))],
    summary="Update user roles",
    description="**Required permission:** `user:edit_roles`"
)
async def update_user_roles(
    user_id: str,
    roles: list[str] = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user_repo.set_roles(user_id, roles)
    return {"detail": "User roles updated"}

@router.get(
    "/logs",
    dependencies=[Depends(requires_permission("log:view"))],
    summary="View system logs",
    description="Requires the 'log:view' permission.",
    responses={
        200: {"description": "List of system logs"},
        403: {"description": "Permission denied"}
    }
)
async def get_system_logs(db: AsyncSession = Depends(get_db)):
    log_repository = LogRepository(db)
    logs = await log_repository.get_all_logs()
    return logs
