from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import OAuthProvider, User
from app.repository import UserRepository
from app.schemas import UserCreate


@pytest.fixture
def user_create() -> UserCreate:
    return UserCreate(
        email=f"test-email-{uuid4()}@example.com",
        username=f"test-username-{uuid4()}",
        name=f"test-name-{uuid4()}",
        profile_picture=f"test-picture-{uuid4()}",
    )


@pytest.mark.integration
async def test_create_user(
    user_repository: UserRepository, user_create: UserCreate
) -> None:
    user = await user_repository.create_user(user=user_create)
    assert user.id is not None


@pytest.mark.integration
async def test_get_error_without_loading_providers(
    test_user_with_oauth_provider: tuple[User, OAuthProvider],
) -> None:
    user, _ = test_user_with_oauth_provider
    with pytest.raises(InvalidRequestError, match="lazy='raise'"):
        _ = user.providers


@pytest.mark.integration
async def test_get_user_with_providers(
    db_session: AsyncSession,
    test_user_with_oauth_provider: tuple[User, OAuthProvider],
) -> None:
    user, provider = test_user_with_oauth_provider

    stmt = select(User).where(User.id == user.id).options(selectinload(User.providers))

    result = await db_session.execute(stmt)
    user = result.scalar_one()

    assert user.providers
    assert user.providers[0] == provider


@pytest.mark.integration
async def test_repeat_username_failed(
    user_repository: UserRepository, test_user: User
) -> None:
    user_in = UserCreate(
        name=test_user.name if test_user.name else "",
        username=test_user.username,
        email=f"test-different-{uuid4()}@example.com",
        profile_picture=test_user.profile_picture,
    )
    with pytest.raises(IntegrityError):
        await user_repository.create_user(user_in)


@pytest.mark.integration
async def test_get_user_by_id(test_user: User, user_repository: UserRepository) -> None:
    exists_user = await user_repository.get_user_by_id(test_user.id)

    assert exists_user is not None
    assert test_user.id == exists_user.id
    assert test_user.email == exists_user.email
