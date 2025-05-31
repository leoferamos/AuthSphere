from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
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
    active_fields: dict = Depends(get_active_fields),
    request: Request = None
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
    # Log: user created
    log_repo = LogRepository(db)
    await log_repo.create_log(
        user_id=user.id,
        action="user_created",
        ip_address=request.client.host if request else None,
        details=f"username={user.username}, email={user.email}"
    )
    return user

@router.delete(
    "/users/{user_id}",
    dependencies=[Depends(requires_permission("user:delete"))]
)
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    await user_repo.delete_user(user_id)
    # Log: user deleted
    log_repo = LogRepository(db)
    await log_repo.create_log(
        user_id=user_id,
        action="user_deleted",
        ip_address=request.client.host if request else None
    )
    return {"status": "success"}

@router.patch(
    "/users/{user_id}/roles",
    dependencies=[Depends(requires_permission("user:edit_roles"))],
    summary="Update user roles",
    description="**Required permission:** `user:edit_roles`"
)
async def update_user_roles(
    user_id: str,
    roles: list[str] = Body(..., embed=True),
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    user_repo = UserRepository(db)
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user_repo.set_roles(user_id, roles)
    # Log: user roles updated
    log_repo = LogRepository(db)
    await log_repo.create_log(
        user_id=user_id,
        action="user_roles_updated",
        ip_address=request.client.host if request else None,
        details=f"roles={roles}"
    )
    return {"detail": "User roles updated"}

@router.get(
    "/logs",
    dependencies=[Depends(requires_permission("logs:view"))],
    summary="List all audit logs",
    description="Only accessible by users with the 'logs:view' permission."
)
async def list_logs(
    db: AsyncSession = Depends(get_db)
):
    log_repo = LogRepository(db)
    logs = await log_repo.get_all_logs()
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "timestamp": log.timestamp,
            "ip_address": log.ip_address,
            "details": log.details,
        }
        for log in logs
    ]

@router.delete(
    "/users/{user_id}/anonymize",
    summary="Anonymize user account (LGPD)",
    description="Anonymizes all personal data of the user. Only the user or an admin can perform this action.",
    dependencies=[Depends(requires_permission("user:anonymize"))]
)
async def anonymize_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    user_repo = UserRepository(db)
    log_repo = LogRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

   
    user.username = f"anon_{user.id[:8]}"
    user.email = f"anon_{user.id[:8]}@anon.local"
    user.first_name = None
    user.last_name = None
    user.phone = None
    user.date_of_birth = None
    user.hashed_password = ""
    user.is_active = False
    

    await db.commit()

    # Log: user anonymized
    await log_repo.create_log(
        user_id=user.id,
        action="user_anonymized",
        ip_address=request.client.host if request else None
    )

    return {"status": "success", "msg": "User data anonymized"}
