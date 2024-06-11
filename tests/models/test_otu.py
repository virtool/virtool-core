from virtool_core.models.otu import OTUSegment, OTUSequence


def test_molecule_nullable():
    segment = OTUSegment(molecule="", name="RNA 1", required=False)
    assert segment.molecule is None

    segment = OTUSegment(molecule="ssRNA", name="RNA 1", required=False)
    assert segment.molecule == "ssRNA"


def test_host_nullable():
    sequence = {
        "accession": "test_accession",
        "definition": "test_definition",
        "id": "test_id",
        "sequence": "ATCD",
    }

    assert OTUSequence(**sequence).host == ""

    assert OTUSequence(**{**sequence, "host": "test_host"}).host == "test_host"
