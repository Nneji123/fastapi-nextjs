from fastapi import APIRouter
from api.public.towns.routes import towns

router = APIRouter()

router.include_router(towns.router, prefix="/towns")
