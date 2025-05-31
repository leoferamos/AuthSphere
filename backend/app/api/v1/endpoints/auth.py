from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import Token
from app.core.utils.security import create_access_token, verify_password
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.config.database import get_db
from datetime import datetime, timedelta
import secrets
from pydantic import BaseModel

router = APIRouter(tags=["Authentication"])

class PasswordResetRequest(BaseModel):
    email: str

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_username(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    return {
        "access_token": create_access_token(data={"sub": user.username}),
        "token_type": "bearer"
    }

@router.post("/password-reset/request")
async def request_password_reset(
    data: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_email(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)
    await user_repo.set_reset_token(user.id, token, expires)
    # Aqui você enviaria o token por e-mail para o usuário
    return {"msg": "Password reset instructions sent (simulated)", "reset_token": token}

@router.post("/password-reset/confirm")
async def reset_password(token: str, new_password: str, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)
    user = await user_repo.get_by_reset_token(token)
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    await user_repo.update_password(user.id, new_password)
    await user_repo.clear_reset_token(user.id)
    return {"msg": "Password updated successfully"}
