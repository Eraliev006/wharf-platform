from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RefreshTokenRequest(_message.Message):
    __slots__ = ("refresh_token",)
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    refresh_token: str
    def __init__(self, refresh_token: _Optional[str] = ...) -> None: ...

class RefreshTokenResponse(_message.Message):
    __slots__ = ("access_token", "refresh_token")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    refresh_token: str
    def __init__(self, access_token: _Optional[str] = ..., refresh_token: _Optional[str] = ...) -> None: ...

class LoginRequest(_message.Message):
    __slots__ = ("code", "provider")
    class OAuthProvider(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OAUTH_PROVIDER_UNSPECIFIED: _ClassVar[LoginRequest.OAuthProvider]
        OAUTH_PROVIDER_GOOGLE: _ClassVar[LoginRequest.OAuthProvider]
        OAUTH_PROVIDER_GITHUB: _ClassVar[LoginRequest.OAuthProvider]
    OAUTH_PROVIDER_UNSPECIFIED: LoginRequest.OAuthProvider
    OAUTH_PROVIDER_GOOGLE: LoginRequest.OAuthProvider
    OAUTH_PROVIDER_GITHUB: LoginRequest.OAuthProvider
    CODE_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    code: str
    provider: LoginRequest.OAuthProvider
    def __init__(self, code: _Optional[str] = ..., provider: _Optional[_Union[LoginRequest.OAuthProvider, str]] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ("access_token", "refresh_token")
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    refresh_token: str
    def __init__(self, access_token: _Optional[str] = ..., refresh_token: _Optional[str] = ...) -> None: ...

class GetMeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LogoutRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LogoutResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "name", "username", "profile_picture")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PROFILE_PICTURE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    username: str
    profile_picture: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., username: _Optional[str] = ..., profile_picture: _Optional[str] = ...) -> None: ...

class GetMeResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...
