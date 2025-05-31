import asyncio
from logging.config import fileConfig
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config.settings import settings

from app.domain.entities.user import Base, User
from app.domain.entities.role import Role, user_roles
from app.domain.entities.permission import Permission, role_permissions
from app.domain.entities.form_field import FormField
from app.domain.entities.audit_log import AuditLog


config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,  
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    engine = create_async_engine(settings.DB_URL)
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    raise NotImplementedError("Offline migrations are not supported in this setup.")
else:
    run_migrations_online()
