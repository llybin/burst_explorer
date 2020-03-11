from unittest import TestCase

from vcr import VCR

from scan.helpers.pending_txs import get_pending_txs

my_vcr = VCR(
    cassette_library_dir="scan/tests/fixtures/vcr/information",
    record_mode="once",
    decode_compressed_response=True,
)


class GetPendingTxs(TestCase):
    @my_vcr.use_cassette("get_pending_txs.yaml")
    def test_ok(self):
        txs = get_pending_txs()
        self.assertEqual(len(txs), 15)
        self.assertEqual(txs[14]["multiout"], 2)
        self.assertEqual(txs[0]["multiout"], 6)
