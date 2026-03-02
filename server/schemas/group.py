import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from server.database import Base
from server.schemas.enums import GroupRoleEnum
from server.schemas.mixins import TimestampMixin, UUIDMixin


class Group(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    owner: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    members: Mapped[list["UserGroup"]] = relationship(
        "UserGroup", back_populates="group", cascade="all, delete-orphan"
    )


class UserGroup(Base):
    __tablename__ = "user_groups"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), primary_key=True, index=True
    )
    role: Mapped[GroupRoleEnum] = mapped_column(
        ENUM(GroupRoleEnum, name="group_role_enum", create_type=True),
        default=GroupRoleEnum.user,
        nullable=False,
        index=True,
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="groups", foreign_keys=[user_id])
    group: Mapped["Group"] = relationship("Group", back_populates="members", foreign_keys=[group_id])
