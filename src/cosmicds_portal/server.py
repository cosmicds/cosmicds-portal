from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from solara.server.fastapi import app as solapp

SECRET = "super-secret-key"

app = FastAPI()
# manager = LoginManager(SECRET, '/login',
#                        use_cookie=True,
#                        use_header=False)


@app.get("/hello")
def read_root():
    return {"Hello": "World"}


app.mount("/", app=solapp)
