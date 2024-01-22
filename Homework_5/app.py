from fastapi import FastAPI, requests, responses, Path, encoders
from typing import Annotated
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import OperationalError

from models import TaskSchema, Task, db, Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/tasks", response_model=list[TaskSchema])
async def all_tasks(request: requests.Request):
    tasks = db.query(Task).all()
    if tasks:
        all_tasks = encoders.jsonable_encoder(tasks)
        return responses.JSONResponse(content=all_tasks, status_code=200)
    message = {"message": "Not have tasks"}
    return responses.JSONResponse(content=message, status_code=204)


@app.get("/tasks/{id}")
async def task(id: Annotated[int, Path(ge=0)]):
    task = db.query(Task).filter(Task.task_id == id).first()
    return responses.JSONResponse(content=encoders.jsonable_encoder(task))


@app.post("/tasks")
async def add_task(task: TaskSchema):
    exist_task = db.query(Task).filter(Task.task_id == task.task_id).first()
    if exist_task:
        message = {"message": "task exist"}
        return responses.JSONResponse(content=message, status_code=409)
    new_task = Task(
        task_id=task.task_id,
        title=task.title,
        description=task.description,
        status=task.status
    )
    db.add(new_task)
    db.commit()
    message = {"New task": task.task_id}
    return responses.JSONResponse(content=message, status_code=201)


@app.put("/tasks/{id}")
async def update_task(id: Annotated[int, Path(qe=0)], upd_task: TaskSchema = None):
    task = db.query(Task).filter(Task.task_id == id).first()
    if task and upd_task:
        task.task_id = upd_task.task_id
        task.title = upd_task.title
        task.description = upd_task.description
        task.status = upd_task.status
        db.commit()
        message = {"Task": task.task_id}
        return responses.JSONResponse(content=message, status_code=200)
    message = {"Task": None}
    return responses.JSONResponse(content=message, status_code=204)


@app.delete("/tasks/{id}")
async def del_task(id: Annotated[int, Path(qe=0)]):
    task = db.query(Task).filter(Task.task_id == id).first()
    if task:
        db.delete(task)
        db.commit()
        message = {"Task": task.task_id}
        return responses.JSONResponse(content=message, status_code=200)
    message = {"message": "Not exist"}
    return responses.JSONResponse(content=message, status_code=204)


@app.exception_handler(RequestValidationError)
async def not_valid(request: requests.Request, exc: RequestValidationError):
    message = {"error": exc.body}
    return responses.JSONResponse(content=message, status_code=400)


@app.exception_handler(OperationalError)
async def db_not_available(request: requests.Request, exc: OperationalError):
    content = {"error": exc.code}
    return responses.JSONResponse(content=content, status_code=400)
