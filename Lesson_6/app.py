from fastapi import FastAPI, HTTPException
from db_init import shutdown, startup
from sqlalchemy import select as q_select, insert, update, delete as q_delete
from typing import List

from models import User
from schemas import UserInSchema
from db_init import db
from tools import get_password_hash

app = FastAPI()
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.get("/users", response_model=List[UserInSchema])
async def all_users() -> List[User] | dict[str, str]:
    query = q_select(User)
    print(query)
    users = await db.fetch_all(query)
    if users:
        return users
    raise HTTPException(status_code=404, detail="Not have users")


@app.get("/users/{id}", response_model=UserInSchema)
async def user(id: int) -> UserInSchema:
    query  = q_select(User).where(User.id == id)
    print(query)
    user = await db.fetch_one(query)
    if user:
        return user
    raise HTTPException(status_code=404, detail="Not have user")


@app.post("/users/", response_model=UserInSchema)
async def add_user(user: UserInSchema) -> dict[str, int]:
    user_data = user.model_dump()
    user_data["password"] = get_password_hash(user.password)
    query = insert(User).values(**user_data)
    user_id = await db.execute(query, user_data)
    return {**user_data, "id": user_id}


@app.put('/users/{user_id}', response_model=UserInSchema)
async def update_user(user_id: int, user: UserInSchema) -> UserInSchema:
    """Обновление информации о пользователе: PUT /users/{user_id}/"""
    query = q_select(User).where(User.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        updated_user = user.model_dump(exclude_unset=True)
        if 'password' in updated_user:
                updated_user['password'] = get_password_hash(updated_user.pop('password'))
        query = update(User).where(User.id == user_id).values(updated_user)
        await db.execute(query)
        return await db.fetch_one(q_select(User).where(User.id == user_id))
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.delete('/users/{user_id}/')
async def delete_user(user_id: int) -> dict:
    """Удаление пользователя: DELETE /users/{user_id}/"""
    query = q_select(User).where(User.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        query = q_delete(User).where(User.id == user_id)
        await db.execute(query)
        return {'detail': f'Пользователь с id={db_user.id} удален'}
    raise HTTPException(status_code=404, detail="Пользователь не найден")
