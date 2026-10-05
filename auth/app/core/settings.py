from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    app_env: Literal["local", "dev", "prod"]

    db_url: str

    redis_host: str
    redis_port: int

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    github_client_id: str
    github_client_secret: str
    github_redirect_uri: str

    jwt_secret_key: str

    # Save in different ways for easy reading
    jwt_access_token_ttl_min: int = 15
    jwt_refresh_token_ttl_day: int = 7

    grpc_server_port: int = 50051

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"


settings = Settings()
