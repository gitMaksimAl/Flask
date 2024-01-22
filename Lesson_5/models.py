from typing import Optional
from pydantic import (
    BaseModel, Field, EmailStr
)
from sqlalchemy import create_engine, Column, Integer, String, Boolean, BINARY
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///lesson5.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": True})

Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    title = Column(String(80), nullable=False)
    description = Column(String(80), nullable=False)
    status = Column(String(80), nullable=False)
    is_del = Column(Boolean, nullable=False)


class TaskSchema(BaseModel):
    task_id: int
    title: Optional[str] = None
    description: str
    status: Optional[str] = None


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(12), nullable=False)
    email = Column(String(255), nullable=False)
    passwd = Column(BINARY(60), nullable=False)

    def __repr__(self):
        return f"User({self.name}, {self.email}"


class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str = Field(default=None, title="Name", max_length=12)
    email: EmailStr = Field(default=None, title="Email", max_length=254)
    passwd: str = Field(default=None, title="Password", min_leght=8, max_length=12)
    confirm: str = Field(default=None, title="Password", min_leght=8, max_length=12)

    class Config:
        orm_mode = True
