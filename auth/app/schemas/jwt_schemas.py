from pydantic import BaseModel


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class Token(BaseModel):
    token: str


class TokenPairs(BaseModel):
    access_token: Token
    refresh_token: Token
