from uuid import uuid4

import pytest

from app.models import OAuthProvider, User
from app.models.oauth_provider import OAuthProviders
from app.repository import OAuthProviderRepository
from app.schemas import OAuthProviderCreate


@pytest.fixture
def provider_create() -> OAuthProviderCreate:
    return OAuthProviderCreate(provider=OAuthProviders.GITHUB, provider_id=str(uuid4()))


@pytest.mark.integration
async def test_create_oauth_provider(
    oauth_provider_repository: OAuthProviderRepository,
    provider_create: OAuthProviderCreate,
    test_user: User,
) -> None:
    provider = await oauth_provider_repository.create_provider(
        provider_create, test_user.id
    )

    assert provider.id is not None


@pytest.mark.integration
async def test_find_user_by_provider(
    test_user_with_oauth_provider: tuple[User, OAuthProvider],
    oauth_provider_repository: OAuthProviderRepository,
) -> None:
    created_user, provider = test_user_with_oauth_provider

    user = await oauth_provider_repository.find_user_by_provider(
        provider=provider.provider, provider_id=provider.provider_id
    )

    assert user is not None
    assert user.id == created_user.id
    assert user.id == provider.user_id
