import asyncio
import signal

import grpc
import structlog
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection

from app.core import configure_logger, settings
from app.generated.auth.v1 import auth_pb2, auth_pb2_grpc
from app.services.servicer import AuthServicer

log = structlog.get_logger()


def create_server(
    port: int,
) -> tuple[grpc.aio.Server, health.aio.HealthServicer, int]:
    server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServicer(), server)
    health_servicer = health.aio.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    if settings.app_env == "local" or settings.app_env == "dev":
        service_names = (
            auth_pb2.DESCRIPTOR.services_by_name["AuthService"].full_name,
            reflection.SERVICE_NAME,
            health.SERVICE_NAME,
        )
        log.info("reflection enabled", app_env=settings.app_env)
        reflection.enable_server_reflection(service_names, server)

    bound_port = server.add_insecure_port(f"[::]:{port}")

    return (server, health_servicer, bound_port)


async def serve() -> None:
    server, health_servicer, port = create_server(settings.grpc_server_port)

    log.info("start_server")
    await server.start()
    await health_servicer.set(
        service="auth.v1.AuthService", status=health_pb2.HealthCheckResponse.SERVING
    )
    log.info("server_started", port=port)

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop.set)
    await stop.wait()
    await health_servicer.enter_graceful_shutdown()
    await server.stop(grace=5)
    log.info("server_stopped")


def main() -> None:
    configure_logger()
    log.info("Started app")
    asyncio.run(serve())
