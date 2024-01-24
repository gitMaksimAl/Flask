from fastapi import FastAPI

app2 = FastAPI()


@app2.get("/")
async def get_all_items():
    ...


@app2.get("/{id}")
async def get_item(id: int):
    ...
