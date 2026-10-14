import grpc
import pytest
from grpc_health.v1 import health, health_pb2
from grpc_health.v1.health_pb2_grpc import HealthStub


@pytest.mark.smoke
async def test_server_is_health(
    test_server_health: tuple[grpc.aio.Server, health.aio.HealthServicer, int],
) -> None:
    _, _, port = test_server_health
    async with grpc.aio.insecure_channel(f"localhost:{port}") as channel:
        stub = HealthStub(channel=channel)
        response = await stub.Check(
            health_pb2.HealthCheckRequest(service="auth.v1.AuthService")
        )

        assert response.status == health_pb2.HealthCheckResponse.SERVING
