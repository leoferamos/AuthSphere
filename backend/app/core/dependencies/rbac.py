from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config.database import get_db
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.dependencies.auth import get_current_user
from fastapi import APIRouter

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

def requires_permission(permission: str):
    async def dependency(
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
    ):
        user_repo = UserRepository(db)
        if not await user_repo.has_permission(current_user.id, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return dependency

@router.patch(
    "/users/{user_id}/roles",
    dependencies=[Depends(requires_permission("user:edit_roles"))]
)
async def update_user_roles(user_id: int, roles: list, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    await user_repo.update_roles(user_id, roles)
    return {"msg": "User roles updated successfully"}
