import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from .oauth_provider import OAuthProvider


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str | None] = mapped_column(String(50))
    email: Mapped[str | None] = mapped_column(index=True, unique=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    profile_picture: Mapped[str | None] = mapped_column(String)

    providers: Mapped[list["OAuthProvider"]] = relationship(
        "OAuthProvider", back_populates="user", lazy="raise"
    )
