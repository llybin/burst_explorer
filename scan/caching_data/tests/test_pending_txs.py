import pytest

from scan.caching_data.pending_txs import CachingPendingTxs


@pytest.mark.django_db
@pytest.mark.vcr
def test_caching_data():
    txs = CachingPendingTxs().cached_data
    assert len(txs) == 15
    assert txs[14]["multiout"] == 2
    assert txs[0]["multiout"] == 6
