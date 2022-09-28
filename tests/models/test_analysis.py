from datetime import datetime

import pytest

from virtool_core.models.analysis import AnalysisMinimal


@pytest.fixture
def mock_analysis():
    return {
        "created_at": datetime(2022, 8, 16),
        "id": "s3wnp1py",
        "index": {"id": "u3lm1rk8", "version": 14},
        "job": {"id": "1sm20zpm"},
        "ready": False,
        "reference": {"id": "d19exr83", "name": "New Plant Viruses"},
        "sample": {"id": "z5oegpww"},
        "subtractions": [{"id": "1sk885at", "name": "Vitis vinifera"}],
        "user": {"administrator": True, "active": True, "handle": "mrott", "id": "ihvze2u9"},
        "workflow": "pathoscope_bowtie",
    }


def test_default_updated_at(mock_analysis):
    """
    Tests if the 'updated_at' field is set to 'created_at' as default if not given.
    """

    analysis = AnalysisMinimal(**mock_analysis)

    assert analysis.updated_at == analysis.created_at


def test_preset_updated_at(mock_analysis):
    """
    Tests that the 'updated_field' is not set automatically to 'created_at'
    despite being provided.
    """

    mock_analysis.update({"updated_at": datetime(2022, 7, 15)})

    analysis = AnalysisMinimal(**mock_analysis)

    assert analysis.updated_at != analysis.created_at
