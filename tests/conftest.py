import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from server.config import settings
from server.database import Base


@pytest_asyncio.fixture()
async def db_session():
    """
    Creates an independent database session for each test.
    Wraps the whole test in a transaction and rolls it back at the end.
    """
    engine = create_async_engine(settings.database_url, echo=False)
    connection = await engine.connect()
    
    # Standard nested transaction block for isolated tests
    trans = await connection.begin()
    
    Session = async_sessionmaker(
        bind=connection, expire_on_commit=False, class_=AsyncSession
    )
    session = Session()

    yield session

    await session.close()
    await trans.rollback()
    
    await connection.close()
    await engine.dispose()
