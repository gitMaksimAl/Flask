from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import EmailStr

Base = declarative_base()


class User(Base):
    __tablename__ = "users_task"
    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String(50), unique=True, index=True)
    email: str = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def __str__(self):
        return self.username

    def __repr__(self):
        f"User(id={self.id}, username='{self.username}', email='{self.email}')"
