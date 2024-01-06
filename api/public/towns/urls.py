from fastapi import APIRouter
from api.public.towns.routes import towns

townrouter = APIRouter()

townrouter.include_router(towns.router, prefix="/towns")
