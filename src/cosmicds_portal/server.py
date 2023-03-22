from fastapi import FastAPI
from solara.server.fastapi import app as solapp

app = FastAPI()


@app.get("/hello")
def read_root():
    return {"Hello": "World"}


app.mount("/", app=solapp)
