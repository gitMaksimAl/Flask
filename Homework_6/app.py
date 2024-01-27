from fastapi import FastAPI, HTTPException
from typing import List, Union, Dict
from sqlalchemy import select as db_select
from db_init import startup, shutdown
from models import Item
from schemas import ItemSchema
from db_init import async_session as db_session

app = FastAPI()
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.get("/", response_model=List[ItemSchema])
async def get_all_items() -> List[Item] | HTTPException:
    async with db_session() as db:
        result = await db.execute(db_select(Item))
        items = result.scalars().all()
        if items:
            return items
        raise HTTPException(status_code=404, detail="Not have items")


@app.get("/{id}", response_model=ItemSchema)
async def get_item(id: int) -> Item | HTTPException:
    async with db_session() as db:
        item = await db.get(Item, id)
        if item:
            return item
        raise HTTPException(status_code=404, detail="Not have this item")


@app.post("/", response_model=ItemSchema)
async def add_item(item: ItemSchema) -> Item | HTTPException:
    async with db_session(expire_on_commit=False) as db:
        new_item = Item(title=item.title, description=item.description, price=item.price)
        db.add(new_item)
        await db.flush()
        await db.refresh(new_item)
        await db.commit()
        return new_item


@app.put("/{id}", response_model=ItemSchema)
async def update_item(id: int, new_item: ItemSchema) -> Item | HTTPException:
    async with db_session(expire_on_commit=False) as db:
        item = await db.get(Item, id)
        if item:
            item.title = new_item.title
            item.description = new_item.description
            item.price = new_item.price
            await db.flush()
            await db.resfresh(item)
            await db.commit()
            return item
        raise HTTPException(status_code=404, detail="Not have this item")


@app.delete("/{id}", response_model=ItemSchema)
async def delete_item(id: int) -> Item | HTTPException:
    async with db_session(autoflush=True, expire_on_commit=False) as db:
        item = await db.get(Item, id)
        if item:
            await db.delete(item)
            await db.commit()
            return item
        raise HTTPException(status_code=404, detail="Have not this item")
