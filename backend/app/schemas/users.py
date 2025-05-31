from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8, max_length=128)

class UserRead(BaseModel):
    id: str
    username: str
    email: str

    class Config:
        from_attributes = True  

class UserRoleUpdate(BaseModel):
    roles: list[str]  # List of role names, e.g., ["admin", "auditor"]
