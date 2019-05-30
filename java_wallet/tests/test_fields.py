from datetime import datetime

from django.test import TestCase

from java_wallet.fields import (
    PositiveBigIntegerField,
    TimestampField,
    get_desc_tx_type,
)


class PositiveBigIntegerFieldTest(TestCase):
    MAX_BIGINT = 9223372036854775807
    MAX_UBIGINT = 18446744073709551615

    def setUp(self) -> None:
        self.field = PositiveBigIntegerField()

    def test_min_max(self):
        self.assertEqual(self.field.formfield().min_value, 0)

        self.assertEqual(self.MAX_UBIGINT, int('1' * 8 * 8, 2))
        self.assertEqual(self.field.formfield().max_value, self.MAX_UBIGINT)

    def test_from_db_value(self):
        self.assertEqual(self.field.from_db_value(None, None, None), None)

        self.assertEqual(self.field.from_db_value(self.MAX_UBIGINT, None, None), self.MAX_UBIGINT)
        self.assertEqual(self.field.from_db_value(2, None, None), 2)
        self.assertEqual(self.field.from_db_value(1, None, None), 1)
        self.assertEqual(self.field.from_db_value(0, None, None), 0)
        self.assertEqual(self.field.from_db_value(-1, None, None), self.MAX_UBIGINT)
        self.assertEqual(self.field.from_db_value(-2, None, None), self.MAX_UBIGINT - 1)

    def test_get_prep_value(self):
        self.assertEqual(self.field.get_prep_value('1'), 1)
        self.assertEqual(self.field.get_prep_value(None), None)

        self.assertEqual(self.field.get_prep_value(self.MAX_UBIGINT - 1), -2)
        self.assertEqual(self.field.get_prep_value(self.MAX_UBIGINT), -1)
        self.assertEqual(self.field.get_prep_value(2), 2)
        self.assertEqual(self.field.get_prep_value(1), 1)
        self.assertEqual(self.field.get_prep_value(0), 0)
        self.assertEqual(self.field.get_prep_value(self.MAX_BIGINT - 1), self.MAX_BIGINT - 1)
        self.assertEqual(self.field.get_prep_value(self.MAX_BIGINT), self.MAX_BIGINT)
        self.assertEqual(self.field.get_prep_value(self.MAX_BIGINT + 1), -1 * self.MAX_BIGINT - 1)


class TimestampFieldTest(TestCase):
    def setUp(self) -> None:
        self.field = TimestampField()

    def test_from_db_value(self):
        self.assertEqual(
            self.field.from_db_value(0, None, None),
            datetime.fromtimestamp(1407722400))

    def test_get_prep_value(self):
        self.assertEqual(
            self.field.get_prep_value(datetime.fromtimestamp(1407722400)),
            0)


class GetTxDescByTypes(TestCase):
    def test_ok(self):
        self.assertEqual(get_desc_tx_type(0, 1), "Multiout Payment")

    def test_unknown(self):
        self.assertEqual(get_desc_tx_type(15, 88), "Unknown type")
