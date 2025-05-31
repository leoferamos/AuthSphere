from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api
from app.core.config.settings import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.api_router, prefix="/api/v1")
