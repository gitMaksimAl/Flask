from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_all_users():
    return {"message": "Hello World"}


@app.get("/{id}")
async def get_user(name: str):
    return {"message": f"Hello {name}"}
