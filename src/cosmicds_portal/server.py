import httpx
from fastapi import Depends, FastAPI
from fastapi import Request
from fastapi.responses import RedirectResponse
from solara.server.fastapi import app as solapp

from .db import User, create_db_and_tables
from .schemas import UserCreate, UserRead, UserUpdate
from .users import (
    SECRET,
    auth_backend,
    current_active_user,
    fastapi_users,
    google_oauth_client,
)

CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
CALLBACK_URL = "http://your-callback-url"

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["auth"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()


@app.get("/hello")
def read_root():
    return {"Hello": "World"}


@app.get("/auth")
def login(request: Request):
    # Generate the CILogon authorization URL
    authorization_url = f"https://cilogon.org/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={CALLBACK_URL}"

    # Redirect the user to the CILogon authentication page
    return RedirectResponse(authorization_url)


@app.get("/auth/callback")
async def callback(code: str, request: Request):
    # Exchange the authorization code for an access token
    token_endpoint = "https://cilogon.org/oauth2/token"
    token_params = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": CALLBACK_URL,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_endpoint, data=token_params)

    response.raise_for_status()
    access_token = response.json()["access_token"]

    # Retrieve user information using the access token
    userinfo_endpoint = "https://cilogon.org/oauth2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(userinfo_endpoint, headers=headers)

    response.raise_for_status()
    userinfo = response.json()

    # Process user information and create a session for the user
    # (Note: This is a simplified example, you may need to implement your own logic here)

    # Return a response to the authenticated user
    return {"message": f"Hello, {userinfo['name']}!"}


app.mount("/", app=solapp)
