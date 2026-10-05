import uuid

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate

log = structlog.get_logger()


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        log.info("init_user_repo")
        self._session = session

    async def create_user(self, user: UserCreate) -> User:
        log.info("create_user", user=user)
        user_in = User(**user.model_dump())
        self._session.add(user_in)
        await self._session.flush()
        return user_in

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        log.info("get_user_by_id", user_id=user_id)
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
