from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
from datetime import datetime


class UserSchema(BaseModel):

    firstname: str = Field(title="First name", pattern=r"^[A-Z][a-z]*")
    lastname: str = Field(title="Last name", pattern=r"^[A-Z][a-z]*")
    email: EmailStr = Field(title="Email", max_length=254)
    password: str = Field(title="Password", min_length=8, max_length=59)


class ItemSchema(BaseModel):

    title: str = Field(title="Item name", max_length=11)
    description: str = Field(title="Item description", max_length=49)
    price: float = Field(title="Item price")


class OrderSchema(BaseModel):

    user_id: int = Field(title="User id")
    item_id: int = Field(title="Item id")
    order_date: datetime = Field(title="Order date")
    status: str = Field(title="Order status", max_length=11)
