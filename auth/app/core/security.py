import uuid
from datetime import UTC, datetime, timedelta
from typing import Literal

import jwt
import structlog

from app.core.settings import settings
from app.exceptions import InvalidToken, InvalidTokenType, TokenExpired
from app.schemas import Token, TokenPairs

log = structlog.get_logger()

ALGORITHM = "HS256"


def _create_token(
    exp: timedelta, user_id: uuid.UUID, type: Literal["access", "refresh"]
) -> Token:
    expire = datetime.now(UTC) + exp
    token = jwt.encode(
        payload={"sub": str(user_id), "exp": expire, "type": type},
        key=settings.jwt_secret_key,
        algorithm=ALGORITHM,
    )

    return Token(token=token)


def _decode_token(
    token: str,
    type: Literal["access", "refresh"],
) -> uuid.UUID:
    try:
        payload = jwt.decode(
            token,
            key=settings.jwt_secret_key,
            algorithms=[ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        log.warning("expired_token")
        raise TokenExpired("Token expired") from None
    except jwt.InvalidTokenError:
        log.warning("invalid_token")
        raise InvalidToken("Token is not valid") from None

    if payload.get("type") != type:
        raise InvalidTokenType("Invalid token type")

    try:
        return uuid.UUID(payload["sub"])
    except (KeyError, TypeError, ValueError):
        log.warning("invalid_token_subject")
        raise InvalidToken("Invalid token subject") from None


def decode_access_token(token: str) -> uuid.UUID:
    return _decode_token(token=token, type="access")


def decode_refresh_token(token: str) -> uuid.UUID:
    return _decode_token(token=token, type="refresh")


def create_access_token(user_id: uuid.UUID) -> Token:
    token = _create_token(
        exp=timedelta(minutes=settings.jwt_access_token_ttl_min),
        user_id=user_id,
        type="access",
    )
    return token


def create_refresh_token(user_id: uuid.UUID) -> Token:
    return _create_token(
        exp=timedelta(days=settings.jwt_refresh_token_ttl_day),
        user_id=user_id,
        type="refresh",
    )


def refresh_tokens(refresh_token: str) -> TokenPairs:
    user_id = _decode_token(token=refresh_token, type="refresh")
    return TokenPairs(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )
