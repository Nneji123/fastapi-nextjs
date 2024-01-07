from fastapi import APIRouter
from api.public.towns.routes import router as townrouter
from api.public.people.routes import router as peoplerouter


public_router = APIRouter()

public_router.include_router(peoplerouter, prefix="/people", tags=["People"])
public_router.include_router(townrouter, prefix="/towns", tags=["Towns"])
