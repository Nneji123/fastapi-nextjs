# main.py (or your FastAPI endpoint file)

from fastapi import Depends, APIRouter
from api.auth.kindeauth import get_access_token

privaterouter = APIRouter(prefix="/private", tags=["Private"])


# async def secure_endpoint(current_user: dict = Depends(get_current_user)):
#     user_email = current_user.get("email")
#     return {"message": f"Authenticated user's email: {user_email}"}

@privaterouter.get("/secure_endpoint")
async def secure_endpoint(token: str = Depends(get_access_token)):
    # Your code logic for the secure endpoint goes here
    return {"token": token}
