from sqlalchemy import Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.core.config.database import Base

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String(36), ForeignKey("roles.id"), index=True),
    Column("permission_name", String(50), ForeignKey("permissions.name"), index=True)
)

class Permission(Base):
    __tablename__ = "permissions"

    name = Column(String(50), primary_key=True) 
    description = Column(String(100))

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
