from fastapi import APIRouter
from api.public.people.routes import router

people_router = APIRouter()

people_router.include_router(router, prefix="/people", tags=["People"])
