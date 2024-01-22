from fastapi import FastAPI, responses, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from pydantic import EmailStr
import bcrypt

from models import User, db, Base, engine

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates("./templates")
app3 = FastAPI()


@app3.get("/login")
async def login(
        request: Request,
        name: str = Form(max_length=12),
        email: str = Form(max_length=254),
        password: str = Form(max_length=12),
):
    user = db.query(User).filter(User.name == name,
                                 User.email == email).first()
    if user and bcrypt.checkpw(user.passwd,
                               bcrypt.hashpw(bytes(password), bytes(email))):
        return templates.TemplateResponse("home.html",
                                          {"request": request, "user": name})
    return responses.RedirectResponse(request.url_for("login"), status_code=403)


@app3.get("/")
async def users(request: Request, name: str = None):
    if not name:
        name = "stranger"
    return templates.TemplateResponse("home.html",
                                      {"request": request, "name": name})


@app3.post("/")
async def add_user(
        request: Request,
        name: str = Form(max_length=12),
        email: EmailStr = Form(max_length=254),
        password: str = Form(min_length=8, max_length=12),
        confirm: str = Form(min_length=8, max_length=12)
):
    if password != confirm:
        return templates.TemplateResponse(
            "home.html",
            {"request": request, "message": "password not match"}
        )
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse(
            "home.html",
            {"request": request, "message": "user exist"}
        )
    user = User(
        name=name,
        email=email,
        passwd=bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    )
    db.add(user)
    db.commit()
    return templates.TemplateResponse("home.html",
                                      {"request": request, "name": user.name})


@app3.exception_handler(RequestValidationError)
async def email_error(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "message": exc.errors()}
    )
