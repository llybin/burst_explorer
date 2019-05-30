from django.db import models

from java_wallet.fields import PositiveBigIntegerField, TimestampField


class MultiOut(models.Model):
    id = models.BigAutoField(primary_key=True)
    tx_id = PositiveBigIntegerField(db_index=True)
    height = models.IntegerField(db_index=True)
    sender_id = PositiveBigIntegerField(db_index=True)
    recipient_id = PositiveBigIntegerField(db_index=True)
    amount = PositiveBigIntegerField()
    tx_type = models.PositiveSmallIntegerField()
    block_timestamp = TimestampField()
