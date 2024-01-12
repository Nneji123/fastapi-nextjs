from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter


from api.public.people.routes import router as peoplerouter
from api.public.towns.routes import router as townrouter


public_router = APIRouter()

@public_router.get("/rate_limit", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def test_rate_limit():
    return {"Hello": "This is a  rate limited endpoint!"}


public_router.include_router(peoplerouter, prefix="/people", tags=["People"])
public_router.include_router(townrouter, prefix="/towns", tags=["Towns"])
