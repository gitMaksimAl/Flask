from fastapi import FastAPI
from sqlalchemy import select as db_select
from fastapi.exceptions import HTTPException
from typing import List
from datetime import datetime

from db_init import async_session as db_session
from models import Order, User, Item
from schemas import OrderSchema, OrderInfo

app3 = FastAPI()


@app3.get("/", response_model=List[OrderSchema])
async def get_all_orders() -> List[OrderSchema] | HTTPException:
    async with db_session() as db:
        result = await db.execute(db_select(Order).order_by(Order.id))
        orders = result.scalars().all()
        if orders:
            return orders
        raise HTTPException(status_code=404, detail="Have not any order")


@app3.get("/{id}", response_model=OrderInfo)
async def get_order(id: int) -> OrderInfo | HTTPException:
    async with db_session() as db:
        query = db_select(
            Order.order_date, Order.status,
            User.firstname, User.lastname, User.email,
            Item.title, Item.description, Item.price
        ).join(User).join(Item).where(Order.id == id)
        print(f"QUERY: {query}")
        result = await db.execute(query)
        order = result.fetchone()
        if order:
            return order
        raise HTTPException(status_code=404, detail="Not have this order")


@app3.post("/", response_model=OrderSchema)
async def add_order(order: OrderSchema) -> Order | HTTPException:
    async with db_session(expire_on_commit=False) as db:
        new_order = Order(user_id=order.user_id, item_id=order.item_id,
                          order_date=datetime.now(), status=order.status)
        db.add(new_order)
        await db.flush()
        await db.refresh(new_order)
        await db.commit()
        return new_order


@app3.put("/{id}", response_model=OrderSchema)
async def update_order(id: int,
                       new_order: OrderSchema) -> Order | HTTPException:
    async with db_session(expire_on_commit=False) as db:
        order = await db.get(Order, id)
        if order:
            order.user_id = new_order.user_id
            order.item_id = new_order.item_id
            order.order_date = new_order.order_date
            order.status = new_order.status
            await db.flush()
            await db.refresh(order)
            await db.commit()
            return order
        raise HTTPException(status_code=404, detail="Not have this order")


@app3.delete("/{id}", response_model=OrderSchema)
async def delete_order(id: int) -> Order | HTTPException:
    async with db_session(autoflush=True, expire_on_commit=False) as db:
        order = await db.get(Order, id)
        if order:
            await db.delete(order)
            await db.commit()
            return order
        raise HTTPException(status_code=404, detail="Have not this order")
