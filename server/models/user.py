import uuid
from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database import Base
from server.models.enums import AuthProviderEnum, GlobalRoleEnum
from server.models.mixins import TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    provider: Mapped[AuthProviderEnum] = mapped_column(
        ENUM(AuthProviderEnum, name="auth_provider_enum", create_type=True), nullable=False
    )
    google_id: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True, index=True)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    global_role: Mapped[GlobalRoleEnum] = mapped_column(
        ENUM(GlobalRoleEnum, name="global_role_enum", create_type=True),
        default=GlobalRoleEnum.user,
        nullable=False,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    verifications: Mapped[list["EmailVerification"]] = relationship(
        "EmailVerification", back_populates="user", cascade="all, delete-orphan"
    )


class EmailVerification(Base, UUIDMixin):
    __tablename__ = "email_verifications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="verifications")
