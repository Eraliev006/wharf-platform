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
        UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(index=True, nullable=True, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    profile_picture: Mapped[str] = mapped_column(String, nullable=True)

    providers: Mapped[list["OAuthProvider"]] = relationship(
        "OAuthProvider", back_populates="user"
    )
