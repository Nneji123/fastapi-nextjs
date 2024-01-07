from fastapi import APIRouter
from api.public.towns.routes import router

town_router = APIRouter()

town_router.include_router(router, prefix="/towns", tags=["Towns"])
