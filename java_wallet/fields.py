import logging
from ctypes import c_long, c_ulong
from datetime import datetime

from django.db.models import BigIntegerField, DateTimeField
from django.utils.translation import ugettext as _

from burst.constants import BLOCK_CHAIN_START_AT
from java_wallet.constants import TX_TYPES


class PositiveBigIntegerField(BigIntegerField):
    description = "Big (8 byte) positive integer"

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "min_value": 0,
                "max_value": BigIntegerField.MAX_BIGINT * 2 + 1,
                **kwargs,
            }
        )

    def get_prep_value(self, value):
        if value is None:
            return value
        value = super().get_prep_value(value)
        if value <= BigIntegerField.MAX_BIGINT:
            return value
        return c_long(value).value

    @staticmethod
    def from_db_value(value, expression, connection):
        if value is None or value >= 0:
            return value
        return c_ulong(value).value


class TimestampField(DateTimeField):
    def get_prep_value(self, value):
        return datetime.timestamp(value) - BLOCK_CHAIN_START_AT

    @staticmethod
    def from_db_value(value, expression, connection):
        if value is None:
            return value

        return datetime.fromtimestamp(value + BLOCK_CHAIN_START_AT)


def get_desc_tx_type(tx_type: int, tx_subtype: int) -> str:
    if (tx_type, tx_subtype) in TX_TYPES:
        return TX_TYPES[(tx_type, tx_subtype)]

    else:
        logging.warning("Unknown transaction type: %d-%d", tx_type, tx_subtype)
        return _("Unknown")
