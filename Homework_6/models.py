from sqlalchemy.orm import as_declarative, declared_attr, relationship, declarative_base
from sqlalchemy import Column, Integer, String, DATETIME, ForeignKey, Float
from datetime import datetime


@as_declarative()
class Base:

    id: int = Column(Integer, default=None, nullable=False, primary_key=True, autoincrement=True)
    __name__: str

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"


class User(Base):

    firstname: str = Column(String(50), nullable=False)
    lastname: str = Column(String(50), nullable=False)
    email: str = Column(String(255), nullable=False)
    password: str = Column(String(60), nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, firstname='{self.firstname}'," \
               f" lastname='{self.lastname}', email='{self.email}'," \
               f" password='{self.password}')"


class Item(Base):

    title: str = Column(String(50), nullable=False)
    description: str = Column(String(255), nullable=False)
    price: float = Column(Float, nullable=False)

    def __repr__(self):
        return f"Item(id={self.id}, title='{self.title}'," \
               f" description='{self.description}', price={self.price})"


class Order(Base):

    user_id: int = Column(Integer, ForeignKey("users.id"))
    item_id: int = Column(Integer, ForeignKey("items.id"))
    order_date: datetime = Column(DATETIME, nullable=False)
    status: str = Column(String(12), nullable=False)

    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, item_id=" \
               f"{self.item_id}, order_date={self.order_date}, status={self.status})"


class Config:

    orm_mode = True

