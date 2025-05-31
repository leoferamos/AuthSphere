from fastapi import FastAPI
from app.api.v1.endpoints import auth, users

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1/users")
