from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config.database import get_db
from app.infrastructure.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

def requires_permission(permission: str):
    async def dependency(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
    ):
        from app.core.dependencies.auth import get_current_user
        current_user = await get_current_user(token=token, db=db)
        user_repo = UserRepository(db)
        if not await user_repo.has_permission(current_user.id, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return dependency
