from sqlalchemy import select as db_select
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from typing import List

from db_init import async_session as db_session
from models import User
from schemas import UserSchema
from services import get_hash

app2 = FastAPI()


@app2.get("/", response_model=List[UserSchema])
async def get_all_users() -> List[User] | HTTPException:
    async with db_session() as db:
        result = await db.execute(db_select(User))
        users = result.scalars().all()
        if users:
            return users
        raise HTTPException(status_code=404, detail="Have not any user")


@app2.get("/{id}", response_model=UserSchema)
async def get_user(id: int) -> User | HTTPException:
    async with db_session() as db:
        user = await db.get(User, id)
        if user:
            return user
        raise HTTPException(status_code=404, detail="Not have this user")


@app2.post("/", response_model=UserSchema)
async def add_user(user: UserSchema) -> User | HTTPException:
    async with db_session(expire_on_commit=False) as db:
        db_user = await db.execute(db_select(User).where(
            User.lastname == user.lastname,
            User.email == user.email
        ))
        if not db_user.first():
            new_user = User(
                firstname=user.firstname,
                lastname=user.lastname,
                email=user.email,
                password=get_hash(user.password)
            )
            db.add(new_user)
            await db.flush()
            await db.refresh(new_user)
            print(f"USER: {new_user}")
            await db.commit()
            return new_user
        raise HTTPException(status_code=500, detail="User exist")


@app2.put("/{id}", response_model=UserSchema)
async def get_all_users(id: int, new_user: UserSchema) -> User | HTTPException:
    async with db_session(expire_on_commit=False) as db:
        user = await db.get(User, id)
        if user:
            user.firstname = new_user.firstname
            user.lastname = new_user.lastname
            user.email = new_user.email
            user.password = get_hash(new_user.password)
            await db.flush()
            await db.refresh(user)
            await db.commit()
            return user
    return HTTPException(status_code=404, detail="Not have this user")


@app2.delete("/{id}", response_model=UserSchema)
async def get_user(id: int) -> User | HTTPException:
    async with db_session(expire_on_commit=False) as db:
        user = await db.get(User, id)
        if user:
            await db.delete(user)
            await db.commit()
            return user
        raise HTTPException(status_code=404, detail="User not exist")
