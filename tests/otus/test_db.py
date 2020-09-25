import pytest
from aiohttp.test_utils import make_mocked_coro

import virtool_core.otus.db


@pytest.mark.parametrize("in_db", [True, False])
@pytest.mark.parametrize("pass_document", [True, False])
async def test_join(in_db, pass_document, mocker, dbi, test_otu, test_sequence, test_merged_otu):
    """
    Test that a otu is properly joined when only a ``otu_id`` is provided.

    """
    await dbi.otus.insert_one(test_otu)
    await dbi.sequences.insert_one(test_sequence)

    m_find_one = mocker.patch.object(
        dbi.otus,
        "find_one",
        make_mocked_coro(test_otu if in_db else None)
    )

    kwargs = dict(document=test_otu) if pass_document else dict()

    joined = await virtool_core.otus.db.join(dbi, "6116cba1", **kwargs)

    assert m_find_one.called != pass_document

    if in_db or (not in_db and pass_document):
        assert joined == test_merged_otu
    else:
        assert joined is None
