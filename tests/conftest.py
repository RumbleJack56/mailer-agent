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


@pytest_asyncio.fixture()
async def user_fixture(db_session: AsyncSession):
    from server.schemas.user import User
    from server.schemas.enums import AuthProviderEnum, GlobalRoleEnum
    
    user = User(
        email="fixture_user@example.com",
        name="Fixture User",
        provider=AuthProviderEnum.email,
        global_role=GlobalRoleEnum.user,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture()
async def group_fixture(db_session: AsyncSession, user_fixture):
    from server.schemas.group import Group
    
    group = Group(
        name="Fixture Group",
        description="A group for testing",
        created_by=user_fixture.id,
    )
    db_session.add(group)
    await db_session.commit()
    await db_session.refresh(group)
    return group
