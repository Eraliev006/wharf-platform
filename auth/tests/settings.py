from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path(__file__).resolve().parent.parent

DB_WHITE_LIST: list[str] = ["wharf_test"]


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", env_file=BASE_PATH / ".env", hide_input_in_errors=True
    )
    test_db_url: str

    @field_validator("test_db_url", mode="before")
    @classmethod
    def _check_db_in_white_list(cls, value: object) -> object:
        if not isinstance(value, str):
            raise ValueError("DB Name not a string")

        db_name = value.split("/")[-1]
        if db_name not in DB_WHITE_LIST:
            raise ValueError("DB name not in white list")

        return value


test_settings = TestSettings()
