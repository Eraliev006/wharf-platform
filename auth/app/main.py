import grpc
import structlog
from grpc_health.v1 import health, health_pb2_grpc
from grpc_reflection.v1alpha import reflection

from app.core import configure_logger, settings
from app.generated.auth.v1 import auth_pb2, auth_pb2_grpc
from app.services.servicer import AuthServicer

log = structlog.get_logger()


async def create_server(
    port: int = settings.grpc_server_port,
) -> tuple[grpc.aio.Server, health.aio.HealthServicer, int]:
    server = grpc.aio.server()
    SERVICE_NAMES = (
        auth_pb2.DESCRIPTOR.services_by_name["AuthService"].full_name,
        reflection.SERVICE_NAME,
        health.SERVICE_NAME,
    )
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServicer(), server)
    health_servicer = health.aio.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    if settings.app_env == "local" or settings.app_env == "dev":
        log.info("reflection enabled", app_env=settings.app_env)
        reflection.enable_server_reflection(SERVICE_NAMES, server)

    bound_port = server.add_insecure_port(f"[::]:{port}")

    return (server, health_servicer, bound_port)


def main() -> None:
    configure_logger()
    log.info("Started app")
    print("HELLO WORLD AUTH")
