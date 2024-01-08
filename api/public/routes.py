from fastapi import APIRouter, Depends

from api.public.people.routes import router as peoplerouter

# from api import auth
from api.public.towns.routes import router as townrouter

import redis.asyncio as redis
import uvicorn
from fastapi import Depends, FastAPI

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

public_router = APIRouter()

@public_router.get("/test/secure", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def test_secure_route():
    return {"Hello": "This is a  rate limited endpoint!"}


public_router.include_router(peoplerouter, prefix="/people", tags=["People"])
public_router.include_router(townrouter, prefix="/towns", tags=["Towns"])
