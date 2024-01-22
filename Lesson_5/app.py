from fastapi import FastAPI
from models import Task, TaskSchema, db, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get('/')
async def home():
    return {"message": "Hello mister Anderson!"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": name}


@app.get("/tasks")
async def tasks():
    res = []
    task = db.query(Task).all()
    for t in task:
        res.append(
            {"task_id": t.task_id, "title": t.title,
             "description": t.description, "status": t.status}
        )
    return res

