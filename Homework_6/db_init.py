from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import MetaData
import asyncio

from models import User, Item, Order, Base

SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///homework6.db"
DATA_FILE = "MOCK_DATA.csv"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=True,
    connect_args={"check_same_thread": False}
)
async_session = sessionmaker(autocommit=False, bind=engine, class_=AsyncSession)


async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def shutdown():
    await engine.dispose()


async def prepare_data():
    import csv
    async with async_session() as session:
        with open(DATA_FILE, 'r', encoding="utf-8", newline='') as f:
            dialect = csv.Sniffer().sniff(f.read(1024))
            f.seek(0)
            headers = f.readline().rstrip().split(',')
            reader = csv.DictReader(f, fieldnames=headers,
                                    dialect=dialect)
            for row in reader:
                session.add(Item(
                        title=row["title"],
                        description=row["description"],
                        price=row["price"]
                    ))
            await session.commit()


if __name__ == '__main__':
    asyncio.run(startup())
    asyncio.run(prepare_data())
