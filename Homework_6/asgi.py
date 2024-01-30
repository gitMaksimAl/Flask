import uvicorn

from app import app
from app2 import app2
from app3 import app3

app.mount("/users", app2)
app.mount("/orders", app3)


if __name__ == '__main__':
    uvicorn.run("asgi:app", reload=True)
