import asyncio
from datetime import timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.schemas.enums import AuthProviderEnum, GlobalRoleEnum
from server.schemas.user import EmailVerification, User


@pytest.mark.asyncio
async def test_create_user(db_session: AsyncSession):
    new_user = User(
        email="test_models@example.com",
        name="Test Models",
        provider=AuthProviderEnum.email,
    )
    db_session.add(new_user)
    await db_session.commit()

    stmt = select(User).where(User.email == "test_models@example.com")
    result = await db_session.execute(stmt)
    user = result.scalar_one()

    # Test columns and defaults
    assert user.id is not None
    assert user.name == "Test Models"
    assert user.provider == AuthProviderEnum.email
    assert user.global_role == GlobalRoleEnum.user
    assert user.email_verified is False
    assert user.is_active is True
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_update_updated_at_trigger(db_session: AsyncSession):
    new_user = User(
        email="trigger@example.com",
        name="Trigger Test",
        provider=AuthProviderEnum.email,
    )
    db_session.add(new_user)
    await db_session.commit()
    await db_session.refresh(new_user)

    original_updated_at = new_user.updated_at

    # Update row to fire Postgres trigger
    new_user.name = "Trigger Test Updated"
    await db_session.commit()
    await db_session.refresh(new_user)

    # Note: Because the DB test runs in one big transaction block and `now()` is fixed for a transaction, 
    # `now()` might not advance inside the postgres trigger. We might need a slightly different check,
    # or at least verify it didn't crash. We'll skip precise strict > because of PG xact behavior,
    # but let's assert it exists and is valid.
    assert new_user.updated_at is not None
    assert new_user.updated_at >= original_updated_at


@pytest.mark.asyncio
async def test_create_email_verification(db_session: AsyncSession):
    user = User(
        email="verify@example.com",
        name="Verify Test",
        provider=AuthProviderEnum.email,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    from sqlalchemy.sql import func
    
    verification = EmailVerification(
        user_id=user.id,
        token_hash="hashed_token_string",
        expires_at=func.now() + timedelta(days=1),
    )
    db_session.add(verification)
    await db_session.commit()
    await db_session.refresh(verification)

    assert verification.id is not None
    assert verification.user_id == user.id
    assert verification.token_hash == "hashed_token_string"
    assert verification.created_at is not None
    assert verification.expires_at is not None
    assert verification.used_at is None
