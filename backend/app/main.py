from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.api.v1.endpoints import auth

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

app.include_router(auth.router, prefix="/api/v1")
