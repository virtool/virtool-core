import pytest
from pathlib import Path


@pytest.fixture
def test_json_path() -> Path:
    return Path(__file__).parent / "models/json"


@pytest.fixture
def redis_connection_string(request):
    return request.config.getoption("--redis-connection-string")


def pytest_addoption(parser):
    parser.addoption(
        "--redis-connection-string",
        action="store",
        default="redis://localhost:6379",
    )
