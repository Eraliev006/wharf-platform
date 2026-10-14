import grpc

from app.generated.auth.v1 import auth_pb2, auth_pb2_grpc


class AuthServicer(auth_pb2_grpc.AuthServiceServicer):
    async def Login(
        self,
        request: auth_pb2.LoginRequest,
        context: grpc.aio.ServicerContext[
            auth_pb2.LoginRequest, auth_pb2.LoginResponse
        ],
    ) -> auth_pb2.LoginResponse:
        await context.abort(
            code=grpc.StatusCode.UNIMPLEMENTED, details="Login Method not implemented"
        )

    async def GetMe(
        self,
        request: auth_pb2.GetMeRequest,
        context: grpc.aio.ServicerContext[
            auth_pb2.GetMeRequest, auth_pb2.GetMeResponse
        ],
    ) -> auth_pb2.GetMeResponse:
        await context.abort(
            code=grpc.StatusCode.UNIMPLEMENTED, details="GetMe Method not implemented"
        )

    async def Logout(
        self,
        request: auth_pb2.LogoutRequest,
        context: grpc.aio.ServicerContext[
            auth_pb2.LogoutRequest, auth_pb2.LogoutResponse
        ],
    ) -> auth_pb2.LogoutResponse:
        await context.abort(
            code=grpc.StatusCode.UNIMPLEMENTED, details="Logout Method not implemented"
        )

    async def RefreshToken(
        self,
        request: auth_pb2.RefreshTokenRequest,
        context: grpc.aio.ServicerContext[
            auth_pb2.RefreshTokenRequest, auth_pb2.RefreshTokenResponse
        ],
    ) -> auth_pb2.RefreshTokenResponse:
        await context.abort(
            code=grpc.StatusCode.UNIMPLEMENTED,
            details="Refresh Token Method not implemented",
        )
