from django.test import TestCase

from ..reed_solomon import ReedSolomon


class ReedSolomonTest(TestCase):
    def setUp(self) -> None:
        self.rs = ReedSolomon()

    def test_encode_ok(self):
        self.assertEqual(self.rs.encode('0'), 'BURST-2222-2222-2222-22222')
        self.assertEqual(self.rs.encode('18068221563302946825'), 'BURST-MC2B-T33V-7RW5-HRTHP')
        self.assertEqual(self.rs.encode('3027874167156716972'), 'BURST-CFFE-JEYZ-GJRR-4DB3N')
        self.assertEqual(self.rs.encode('14013682333507417429'), 'BURST-2XCP-UQPY-X8GE-ETNY6')
        self.assertEqual(self.rs.encode('5947343067629234287'), 'BURST-SC5H-2BVQ-4KKB-7PB47')

    def test_decode_ok(self):
        self.assertEqual(self.rs.decode('BURST-2222-2222-2222-22222'), '0')
        self.assertEqual(self.rs.decode('BURST-MC2B-T33V-7RW5-HRTHP'), '18068221563302946825')
        self.assertEqual(self.rs.decode('BURST-CFFE-JEYZ-GJRR-4DB3N'), '3027874167156716972')
        self.assertEqual(self.rs.decode('BURST-2XCP-UQPY-X8GE-ETNY6'), '14013682333507417429')
        self.assertEqual(self.rs.decode('BURST-SC5H-2BVQ-4KKB-7PB47'), '5947343067629234287')
