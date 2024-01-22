from uvicorn import run, Config, Server
from fastapi.staticfiles import StaticFiles

from app import app
from app2 import app2
from app3 import app3

app.mount("/app2", app2)
app.mount("/users", app3)
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == '__main__':
    run("asgi:app", reload=True)