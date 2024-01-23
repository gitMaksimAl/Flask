import sqlalchemy
from sqlalchemy.pool import StaticPool
import databases

from models import User

DATABASE_URL = "sqlite:///lesson6.db"
db = databases.Database(DATABASE_URL)
meta = sqlalchemy.MetaData()


async def startup():
    await db.connect()
    engine = sqlalchemy.create_engine(
        DATABASE_URL, echo=True, poolclass=StaticPool,
        connect_args={"check_same_thread": False}
    )
    User.metadata.create_all(engine)


async def shutdown():
    await db.disconnect()
