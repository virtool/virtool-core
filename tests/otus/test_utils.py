import virtool_core.otus.utils


def test_merge_otu(test_otu, test_sequence, test_merged_otu):
    merged = virtool_core.otus.utils.merge_otu(test_otu, [test_sequence])
    assert merged == test_merged_otu