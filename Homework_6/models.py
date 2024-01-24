from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from datetime import datetime

Base = declarative_base()


class User(Base):

    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True)
    firstname: str = Column(String(50), nullable=False)
    lastname: str = Column(String(50), nullable=False)
    email: str = Column(String(255), nullable=False)
    password: str = Column(String(60), nullable=False)


class Items(Base):

    __tablename__ = "items"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(12), nullable=False)
    description: str = Column(String(50), nullable=False)
    price: float = Column(DECIMAL, nullable=False)


class Order(Base):

    __tablename__ = "orders"
    id: int = Column(Integer, primary_key=True)
    user_id: int = relationship("users", back_populates="orders")
    item_id: int = relationship("items", back_populates="orders")
    order_date: datetime = Column(DATETIME, nullable=False)
    status: str = Column(String(12), nullable=False)
