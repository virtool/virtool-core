import pytest

@pytest.mark.parametrize("remove", [True, False])
async def test_patch_to_version(remove, snapshot, dbi,  create_mock_history):
    await create_mock_history(remove=remove)

    app = {
        "db": dbi
    }

    current, patched, reverted_change_ids = await virtool.history.db.patch_to_version(
        app,
        "6116cba1",
        1
    )

    snapshot.assert_match(current)
    snapshot.assert_match(patched)
    snapshot.assert_match(reverted_change_ids)
