import ctypes
from datetime import datetime

from django.db import models


# models.BigIntegerField -> PositiveBigIntegerField
class PositiveBigIntegerField(models.BigIntegerField):
    empty_strings_allowed = False
    description = "Big (8 byte) positive integer"

    def formfield(self, **kwargs):
        defaults = {'min_value': 0,
                    'max_value': models.BigIntegerField.MAX_BIGINT * 2 - 1}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return ctypes.c_long(value).value

    @staticmethod
    def from_db_value(value, expression, connection):
        if value is None:
            return value
        return ctypes.c_ulong(value).value


# timestamp = IntegerField -> timestamp = TimestampField
class TimestampField(models.DateTimeField):
    @staticmethod
    def from_db_value(value, expression, connection):
        if value is None:
            return value

        return datetime.fromtimestamp(value + 1407722400)

    def get_prep_value(self, value):
        return datetime.timestamp(value) - 1407722400
