from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.config.database import get_db
from app.schemas.users import UserRoleUpdate, UserRead
from app.dependencies import require_admin

router = APIRouter(tags=["Admin"])

@router.put(
    "/users/{user_id}/roles",
    response_model=UserRead,
    summary="Update user roles",
    description="**Admins only.** Replace the user's roles with the provided list.",
    responses={
        200: {"description": "Roles updated successfully"},
        404: {"description": "User or role not found"},
        403: {"description": "Access denied"}
    }
)
async def update_user_roles(
    user_id: str,
    role_update: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_admin)
):
    """
    Update a user's roles. Only accessible by admins.
    """
    try:
        user_repo = UserRepository(db)
        await user_repo.set_roles(user_id, role_update.roles)
        updated_user = await user_repo.get_user_by_id(user_id)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))