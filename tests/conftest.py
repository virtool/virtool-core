import pytest
from pathlib import Path

@pytest.fixture
def test_json_path() -> Path:
    return Path(__file__).parent/"models/json"