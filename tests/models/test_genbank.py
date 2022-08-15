import pytest
from pydantic import ValidationError

from virtool_core.models.genbank import Genbank


@pytest.fixture
def mock_genbank():
    return {
        "accession": "KJ406323.1",
        "definition": "Tobacco mosaic virus isolate TMV-tNK coat protein (CP) gene, complete cds",
        "host": "Solanum lycopersicum",
        "sequence": "ATGTCTTACAGTATCACTACTCCATCTCAGTTCGTGTTCTTGTCATCATGGAAATAGAATAACCGGATCTTATAATCGGAGCTCTTTCGAGAGCTCTTCTGGTTTGGTTTGGACCTCTGGTCCTGCAACTTGAN",
    }


@pytest.mark.parametrize("error", [None, "sequence"])
def test_sequence(mock_genbank, error):
    """
    Tests if the `name` field is set to the `id` as default.
    """
    Genbank(**mock_genbank)
    if error:
        with pytest.raises(ValidationError) as err:
            mock_genbank.update({"sequence": "ACGTNF"})
            Genbank(**mock_genbank)
            assert "The format of the sequence is invalid" in str(err)
