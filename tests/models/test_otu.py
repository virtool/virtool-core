from virtool_core.models.otu import OTUSegment


def test_molecule_nullable():
    segment = OTUSegment(**{"molecule": "", "name": "RNA 1", "required": False})
    assert segment.molecule is None

    segment = OTUSegment(**{"molecule": "ssRNA", "name": "RNA 1", "required": False})
    assert segment.molecule == "ssRNA"
