from fastapi import APIRouter, Depends
# from api import auth
from api.public.towns.routes import router as townrouter
from api.public.people.routes import router as peoplerouter
# from propelauth_py.user import User


public_router = APIRouter()

# @public_router.get("/test/secure")
# def test_secure_route(user: User = Depends(auth.auth.require_user)):
#     # auth object comes from init_auth
#     auth.auth.create_access_token(user.user_id, 10)

#     return {"Hello": user.user_id}


public_router.include_router(peoplerouter, prefix="/people", tags=["People"])
public_router.include_router(townrouter, prefix="/towns", tags=["Towns"])
