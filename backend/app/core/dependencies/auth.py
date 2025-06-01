from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from app.core.utils.security import decode_token
from app.core.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config.database import get_db
from app.infrastructure.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

async def get_current_user(
    access_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(access_token)
    if not payload:
        raise credentials_exception
        
    username: str = payload.get("sub")
    if not username:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = await user_repo.get_by_username(username)
    if not user:
        raise credentials_exception
        
    return user
