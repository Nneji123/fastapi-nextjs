from fastapi_auth0 import Auth0, Auth0User
from dotenv import load_dotenv
from os import getenv

load_dotenv

domain = getenv("AUTH0_DOMAIN")
api_audience = "API_AUDIENCE"

authenticate = Auth0(domain='your-tenant.auth0.com', api_audience='your-api-identifier', scopes={'read:blabla': ''})
