import base64
import json
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
import pytest

from app.core import settings
from app.core.security import (
    ALGORITHM,
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    refresh_tokens,
)
from app.exceptions import InvalidToken, InvalidTokenType, TokenExpired


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        jwt=token,
        key=settings.jwt_secret_key,
        algorithms=[ALGORITHM],
    )


@pytest.mark.smoke
def test_create_access_token() -> None:
    user_id = uuid.uuid4()

    created = create_access_token(user_id=user_id)
    decoded = decode_token(created.token)

    assert decoded["sub"] == str(user_id)
    assert decoded["type"] == "access"


@pytest.mark.smoke
def test_create_refresh_token() -> None:
    user_id = uuid.uuid4()

    created = create_refresh_token(user_id=user_id)
    decoded = decode_token(created.token)

    assert decoded["sub"] == str(user_id)
    assert decoded["type"] == "refresh"


@pytest.mark.smoke
def test_access_and_refresh_tokens_have_different_claims() -> None:
    user_id = uuid.uuid4()

    access = create_access_token(user_id=user_id)
    refresh = create_refresh_token(user_id=user_id)

    decoded_access = decode_token(access.token)
    decoded_refresh = decode_token(refresh.token)

    assert decoded_access["exp"] != decoded_refresh["exp"]
    assert decoded_access["type"] == "access"
    assert decoded_refresh["type"] == "refresh"


@pytest.mark.smoke
def test_check_invalid_payload() -> None:
    invalid_token = jwt.encode(
        payload={"invalid": "payload", "type": "access"},
        key=settings.jwt_secret_key,
        algorithm=ALGORITHM,
    )

    with pytest.raises(InvalidToken):
        decode_access_token(invalid_token)


@pytest.mark.smoke
def test_decode_access_token_returns_user_id() -> None:
    user_id = uuid.uuid4()
    token = create_access_token(user_id=user_id)

    decoded_user_id = decode_access_token(token.token)

    assert decoded_user_id == user_id


@pytest.mark.smoke
def test_cannot_decode_refresh_token_as_access() -> None:
    token = create_refresh_token(user_id=uuid.uuid4())

    with pytest.raises(InvalidTokenType):
        decode_access_token(token.token)


@pytest.mark.smoke
def test_rejects_token_with_invalid_signature() -> None:
    token = jwt.encode(
        payload={
            "sub": str(uuid.uuid4()),
            "type": "access",
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        key="wrong-secret",
        algorithm=ALGORITHM,
    )

    with pytest.raises(InvalidToken):
        decode_access_token(token)


@pytest.mark.smoke
def test_rejects_expired_token() -> None:
    token = jwt.encode(
        payload={
            "sub": str(uuid.uuid4()),
            "type": "access",
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        },
        key=settings.jwt_secret_key,
        algorithm=ALGORITHM,
    )

    with pytest.raises(TokenExpired):
        decode_access_token(token)


@pytest.mark.smoke
def test_rejects_unexpected_algorithm() -> None:
    token = jwt.encode(
        payload={
            "sub": str(uuid.uuid4()),
            "type": "access",
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        key=settings.jwt_secret_key,
        algorithm="HS512",
    )

    with pytest.raises(InvalidToken):
        decode_access_token(token)


@pytest.mark.smoke
def test_refresh_tokens() -> None:
    user_id = uuid.uuid4()
    refresh = create_refresh_token(user_id=user_id)

    pairs = refresh_tokens(refresh.token)

    assert decode_access_token(pairs.access_token.token) == user_id
    assert decode_refresh_token(pairs.refresh_token.token) == user_id


@pytest.mark.smoke
def test_access_instead_refresh_denied() -> None:
    user_id = uuid.uuid4()
    access = create_access_token(user_id=user_id)

    with pytest.raises(InvalidToken):
        refresh_tokens(access.token)


@pytest.mark.smoke
def test_rejects_modified_payload() -> None:
    original_token = create_access_token(user_id=uuid.uuid4()).token
    header, payload, signature = original_token.split(".")

    decoded_payload = json.loads(
        base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4))
    )
    decoded_payload["sub"] = str(uuid.uuid4())

    modified_payload = (
        base64.urlsafe_b64encode(
            json.dumps(decoded_payload, separators=(",", ":")).encode()
        )
        .rstrip(b"=")
        .decode()
    )

    tampered_token = f"{header}.{modified_payload}.{signature}"

    with pytest.raises(InvalidToken):
        decode_access_token(tampered_token)
