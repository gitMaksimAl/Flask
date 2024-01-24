from fastapi import FastAPI

app3 = FastAPI()


@app3.get("/")
async def get_all_orders():
    ...


@app3.get("/{id}")
async def get_order(id: int):
    ...
