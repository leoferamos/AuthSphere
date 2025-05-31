from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config.database import get_db
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.dependencies.auth import get_current_user
from app.core.dependencies.rbac import requires_permission

def requires_permission(permission: str):
    async def dependency(
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ):
        user_repo = UserRepository(db)
        if not await user_repo.has_permission(current_user.id, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return dependency
