from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserCreate, UserRead
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.utils.security import get_password_hash
from app.core.config.database import get_db

router = APIRouter(tags=["Users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user with unique username and email.
    """
    user_repo = UserRepository(db)
    if await user_repo.get_by_username(user_in.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )
    if await user_repo.get_by_email(user_in.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user_in.password)
    user = await user_repo.create_user(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
    )
    return user
