import pytest
import json
from pathlib import Path
from virtool_core.models.analysis import Analysis


@pytest.fixture
def expected_json_path(test_json_path) -> Path:
    return test_json_path / "analysis.json"


@pytest.fixture
def expected_json(expected_json_path):
    return expected_json_path.read_text()


async def test_json_compatibility(expected_json, expected_json_path):
    analysis = Analysis.parse_raw(expected_json)
    analysis_from_file = Analysis.parse_file(expected_json_path)

    assert analysis == analysis_from_file
    analysis_dict = analysis.dict(
        exclude_none=True, exclude={"created_at", "updated_at"}
    )
    json_dict = json.loads(expected_json)

    json_dict = {key: value for key, value in json_dict.items() if key in analysis_dict}

    assert analysis_dict == json_dict
