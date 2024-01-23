import uvicorn
from sqlalchemy import select, delete, insert, update

from db_init import startup, db, shutdown
from models import User
from tools import get_password_hash
from app import app


async def prepare():
    query = delete(User)
    await db.execute(query)
    query = insert(User)
    for i in range(10):
        passwd = get_password_hash(f"Superpassword{i**2}")
        new_user = {
            "username": f"user{i}",
            "email": f"user{i}@mail.ru",
            "password": passwd
        }
        await db.execute(query, new_user)


if __name__ == '__main__':
    uvicorn.run("asgi:app", reload=True)
