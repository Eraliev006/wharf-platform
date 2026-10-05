import uuid

from pydantic import BaseModel, ConfigDict

from app.models.oauth_provider import OAuthProviders


class _OAuthProvider(BaseModel):
    provider: OAuthProviders
    provider_id: str

    model_config = ConfigDict(from_attributes=True)


class OAuthProviderCreate(_OAuthProvider):
    pass


class OAuthProviderResponse(_OAuthProvider):
    id: uuid.UUID
