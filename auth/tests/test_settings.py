import pytest

from app.core import settings


@pytest.mark.smoke
def test_settings() -> None:
    assert settings.log_level == "INFO"
