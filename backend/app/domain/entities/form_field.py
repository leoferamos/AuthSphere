from app.core.config.database import Base
from sqlalchemy import Column, String, Boolean

class FormField(Base):
    __tablename__ = "form_fields"

    name = Column(String(50), primary_key=True)
    label = Column(String(100), nullable=False)
    is_required = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    field_type = Column(String(20), default="text")

    def __repr__(self):
        return f"<FormField {self.name}>"
