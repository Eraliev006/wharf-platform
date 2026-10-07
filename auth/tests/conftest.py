from collections.abc import AsyncGenerator, AsyncIterator, Generator
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from app.models import OAuthProvider, User
from app.models.oauth_provider import OAuthProviders
from app.repository import OAuthProviderRepository, UserRepository
from app.schemas import OAuthProviderCreate, UserCreate
from tests.settings import TestSettings


@pytest.fixture(scope="session")
def test_settings() -> TestSettings:
    return TestSettings()


@pytest.fixture(scope="session")
def migrate_database(test_settings: TestSettings) -> Generator[None]:
    BASE_DIR = Path(__file__).resolve().parent.parent

    config = Config(BASE_DIR / "alembic.ini")

    config.set_main_option(
        "sqlalchemy.url",
        test_settings.test_db_url,
    )

    command.upgrade(config, "head")

    yield

    command.downgrade(config, "base")


@pytest_asyncio.fixture(scope="session")
async def db_engine(
    migrate_database: None, test_settings: TestSettings
) -> AsyncIterator[AsyncEngine]:
    test_engine = create_async_engine(test_settings.test_db_url)

    yield test_engine

    await test_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session(
    db_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession]:
    async with AsyncSession(bind=db_engine) as session:
        yield session

        await session.rollback()


@pytest.fixture(scope="function")
def user_repository(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


@pytest.fixture(scope="function")
def oauth_provider_repository(db_session: AsyncSession) -> OAuthProviderRepository:
    return OAuthProviderRepository(db_session)


@pytest_asyncio.fixture(scope="function")
async def test_user(user_repository: UserRepository) -> User:
    user_in = UserCreate(
        email=f"test-email-{uuid4()}@example.com",
        username=f"test-username-{uuid4()}",
        name=f"test-name-{uuid4()}",
        profile_picture=f"test-picture-{uuid4()}",
    )
    user = await user_repository.create_user(user=user_in)

    return user


@pytest_asyncio.fixture(scope="function")
async def test_user_with_oauth_provider(
    oauth_provider_repository: OAuthProviderRepository, test_user: User
) -> tuple[User, OAuthProvider]:
    provider_in = OAuthProviderCreate(
        provider=OAuthProviders.GITHUB, provider_id=str(uuid4())
    )
    provider = await oauth_provider_repository.create_provider(
        provider_in, test_user.id
    )
    return test_user, provider
