import httpx
from fastapi import Depends, FastAPI
from fastapi import Request
from fastapi.responses import RedirectResponse
from solara.server.fastapi import app as solapp

CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
CALLBACK_URL = "http://your-callback-url"

app = FastAPI()


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
