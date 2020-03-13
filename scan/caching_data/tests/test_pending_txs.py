from unittest import TestCase

from vcr import VCR

from scan.caching_data.pending_txs import CachingPendingTxs

my_vcr = VCR(
    cassette_library_dir="scan/caching_data/tests/fixtures/vcr/pending_txs",
    record_mode="once",
    decode_compressed_response=True,
)


class GetPendingTxs(TestCase):
    @my_vcr.use_cassette("pending_txs_success.yaml")
    def test_ok(self):
        txs = CachingPendingTxs().cached_data
        self.assertEqual(len(txs), 15)
        self.assertEqual(txs[14]["multiout"], 2)
        self.assertEqual(txs[0]["multiout"], 6)
