import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.schemas.enums import GroupRoleEnum
from server.schemas.group import Group, UserGroup


@pytest.mark.asyncio
async def test_create_group(db_session: AsyncSession, user_fixture):
    new_group = Group(
        name="Test Group",
        description="Created in test",
        created_by=user_fixture.id,
    )
    db_session.add(new_group)
    await db_session.commit()

    stmt = select(Group).where(Group.name == "Test Group")
    result = await db_session.execute(stmt)
    group = result.scalar_one()

    assert group.id is not None
    assert group.name == "Test Group"
    assert group.description == "Created in test"
    assert group.created_by == user_fixture.id
    assert group.created_at is not None
    assert group.updated_at is not None


@pytest.mark.asyncio
async def test_group_roles(db_session: AsyncSession, user_fixture, group_fixture):
    user_group = UserGroup(
        user_id=user_fixture.id,
        group_id=group_fixture.id,
        role=GroupRoleEnum.admin,
    )
    db_session.add(user_group)
    await db_session.commit()

    stmt = select(UserGroup).where(
        UserGroup.user_id == user_fixture.id,
        UserGroup.group_id == group_fixture.id
    )
    result = await db_session.execute(stmt)
    fetched_ug = result.scalar_one()

    assert fetched_ug.role == GroupRoleEnum.admin
    assert fetched_ug.joined_at is not None
