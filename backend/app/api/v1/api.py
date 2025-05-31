from fastapi import APIRouter
from .endpoints import users, form_fields, auth 

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users")
api_router.include_router(form_fields.router)
api_router.include_router(auth.router) 