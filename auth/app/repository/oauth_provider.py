import uuid

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models import OAuthProvider, User
from app.models.oauth_provider import OAuthProviders
from app.schemas.oauth_provider import OAuthProviderCreate

log = structlog.get_logger()


class OAuthProviderRepository:
    def __init__(self, session: AsyncSession) -> None:
        log.info("init_oauth_provider_repository")
        self._session = session

    async def create_provider(
        self, provider: OAuthProviderCreate, user_id: uuid.UUID
    ) -> OAuthProvider | None:
        log.info("create_provider", provider=provider)
        provider_in = OAuthProvider(**provider.model_dump(), user_id=user_id)
        self._session.add(provider_in)
        await self._session.flush()
        return provider_in

    async def find_user_by_provider(
        self, provider: OAuthProviders, provider_id: str
    ) -> User | None:
        log.info("find_user_by_provider", provider=provider, provider_id=provider_id)
        stmt = (
            select(User)
            .join(OAuthProvider, OAuthProvider.user_id == User.id)
            .where(
                OAuthProvider.provider == provider,
                OAuthProvider.provider_id == provider_id,
            )
        )

        result = await self._session.execute(stmt)
        return result.scalars().one_or_none()
