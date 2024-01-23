from typing import Optional
from pydantic import (
    BaseModel, Field
)
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///homework5.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": True})

Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    title = Column(String(12), nullable=False)
    description = Column(String(254), nullable=False)
    status = Column(String(14), nullable=False)
    is_del = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Task('{self.task_id}', '{self.title}'," \
               f" '{self.description}', '{self.status}')"


class TaskSchema(BaseModel):
    task_id: Optional[int] = Field(qe=0)
    title: str = Field(title="Title", max_length=12)
    description: str = Field(title="Description", max_length=254)
    status: Optional[str] = Field(
        title="Status",
        pattern=r"((not\s)?(completed))",
        default="not completed", max_length=14
    )

