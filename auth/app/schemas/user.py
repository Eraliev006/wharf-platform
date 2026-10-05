import uuid

from pydantic import BaseModel, ConfigDict, EmailStr


class _User(BaseModel):
    email: EmailStr | None
    username: str
    name: str
    profile_picture: str | None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(_User):
    pass


class UserResponse(_User):
    id: uuid.UUID
