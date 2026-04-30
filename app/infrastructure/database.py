from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.DB_URL,
    pool_size=20,
    max_overflow=30,
    echo=settings.MODE == "DEV",
)

async_session_maker = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False
)


async def get_unit_of_work():
    async with async_session_maker() as session:
        yield session
