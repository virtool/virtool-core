import pytest
import virtool_core.history.db

@pytest.mark.parametrize("remove", [True, False])
async def test_patch_to_version(remove, snapshot, dbi,  create_mock_history):
    await create_mock_history(remove=remove)

    current, patched, reverted_change_ids = await virtool_core.history.db.patch_to_version(
        db=dbi,
        data_path=None,
        otu_id="6116cba1",
        version=1
    )

    snapshot.assert_match(current)
    snapshot.assert_match(patched)
    snapshot.assert_match(reverted_change_ids)
