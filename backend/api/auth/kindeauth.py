from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import requests
from dotenv import load_dotenv
import os

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency function to get the access token
def get_access_token():
    your_domain = os.getenv("DOMAIN")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    access_token_url = f"https://fastscraper.kinde.com/oauth2/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(access_token_url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

