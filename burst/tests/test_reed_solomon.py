from django.test import TestCase

from ..reed_solomon import ReedSolomon, ReedSolomonError


class ReedSolomonTest(TestCase):
    def setUp(self) -> None:
        self.rs = ReedSolomon()

    def test_encode_ok(self):
        self.assertEqual(self.rs.encode('0'), '2222-2222-2222-22222')
        self.assertEqual(self.rs.encode('18068221563302946825'), 'MC2B-T33V-7RW5-HRTHP')
        self.assertEqual(self.rs.encode('3027874167156716972'), 'CFFE-JEYZ-GJRR-4DB3N')
        self.assertEqual(self.rs.encode('14013682333507417429'), '2XCP-UQPY-X8GE-ETNY6')
        self.assertEqual(self.rs.encode('5947343067629234287'), 'SC5H-2BVQ-4KKB-7PB47')

    def test_encode_error(self):
        with self.assertRaises(ReedSolomonError):
            self.rs.encode('-1')
            self.rs.encode('!')

        with self.assertRaises(ReedSolomonError):
            self.rs.encode('1' * 21)

        with self.assertRaises(ReedSolomonError):
            self.rs.encode('')

    def test_decode_ok(self):
        self.assertEqual(self.rs.decode('BURST-2222-2222-2222-22222'), '0')
        self.assertEqual(self.rs.decode('BURST-MC2B-T33V-7RW5-HRTHP'), '18068221563302946825')
        self.assertEqual(self.rs.decode('BURST-CFFE-JEYZ-GJRR-4DB3N'), '3027874167156716972')
        self.assertEqual(self.rs.decode('2XCP-UQPY-X8GE-ETNY6'), '14013682333507417429')
        self.assertEqual(self.rs.decode('SC5H-2BVQ-4KKB-7PB47'), '5947343067629234287')

    def test_decode_error(self):
        with self.assertRaises(ReedSolomonError):
            self.rs.decode('-1')
            self.rs.decode('!')

        with self.assertRaises(ReedSolomonError):
            self.rs.decode('1' * 18)

        with self.assertRaises(ReedSolomonError):
            self.rs.decode('!' * 17)

        with self.assertRaises(ReedSolomonError):
            self.rs.decode('')
