from fastapi import FastAPI
from app.api.v1 import api

app = FastAPI()

app.include_router(api.api_router, prefix="/api/v1")
