import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from .user import User


class OAuthProviders(enum.StrEnum):
    GOOGLE = "google"
    GITHUB = "github"


class OAuthProvider(Base):
    __tablename__ = "oauth_providers"
    __table_args__ = (UniqueConstraint("provider", "provider_id"), {"schema": "auth"})

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("auth.users.id", ondelete="CASCADE"),
        nullable=False,
    )
    provider: Mapped[OAuthProviders] = mapped_column(
        Enum(OAuthProviders, schema="auth"), nullable=False
    )
    provider_id: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["User"] = relationship(
        "User", back_populates="providers", lazy="raise"
    )
