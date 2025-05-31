import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.permission import Permission, role_permissions
from app.domain.entities.role import Role, user_roles
from app.domain.entities.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> User | None:
        """Retrieve a user by username."""
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email."""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def create_user(self, username: str, email: str, hashed_password: str) -> User:
        """Create and persist a new user."""
        new_user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            hashed_password=hashed_password,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user

    async def set_roles(self, user_id: str, role_names: list[str]) -> None:
        """
        Replace the user's roles with the provided list of role names.
        """
        async with self.session.begin():
            user = await self.session.get(User, user_id)
            if not user:
                raise ValueError(f"User {user_id} not found")

            new_roles = []
            for role_name in role_names:
                result = await self.session.execute(select(Role).where(Role.name == role_name))
                role = result.scalars().first()
                if not role:
                    raise ValueError(f"Role '{role_name}' not found")
                new_roles.append(role)

            user.roles = new_roles

    async def has_permission(self, user_id: str, permission_name: str) -> bool:
        stmt = (
            select(Permission.name)
            .select_from(Permission)
            .join(role_permissions, Permission.name == role_permissions.c.permission_name)
            .join(Role, role_permissions.c.role_id == Role.id)
            .join(user_roles, Role.id == user_roles.c.role_id)
            .where(
                (user_roles.c.user_id == user_id) &
                (Permission.name == permission_name)
            )
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar() is not None