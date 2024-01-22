from fastapi import FastAPI
from models import Task, TaskSchema, db

app2 = FastAPI()


@app2.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello mister {name}"}


@app2.get("/tasks/{task_id}")
async def task(task_id: int):
    task = db.query(Task).first()
    return {"task_id": task.task_id, "title": task.title,
            "description": task.description, "status": task.status}


@app2.post("/tasks/{task_id}")
async def add_task(task_id: int, task: TaskSchema):
    tasks = db.query(Task).filter(Task.task_id == task_id).all()
    for task in tasks:
        if task.task_id == task_id:
            return {"message": "Task exist"}
    new_task = Task(
        task_id=task.task_id, title=task.title, description=task.description,
        status=task.status, is_del=False
    )
    db.add(new_task)
    db.commit()
    return {"message": str(task_id)}


@app2.delete("/tasks/{task_id}")
async def del_task(task_id: int):
    tasks = db.query(Task).filter(Task.task_id == task_id).all()
    for task in tasks:
        if task.task_id == task_id:
            db.delete(task)
            db.commit()
            return {"message": str(task_id)}
    return {"message": "Task not exist"}


@app2.put("/tasks/{task_id}")
async def update_task(task_id: int, task_upd: TaskSchema):
    task = db.query(Task).filter(Task.task_id == task_id).first()
    if task:
        task.title = task_upd.title
        task.description = task_upd.description
        task.status = task_upd.status
        db.commit()
        return {"message": str(task_id)}
    return {"message": "Task not exist"}