from django.db import models
from django.utils.translation import ugettext as _

from java_wallet.fields import PositiveBigIntegerField


class MultiOut(models.Model):
    class TxSubtype:
        """java_wallet/constants.py"""
        MULTI_OUT = 1
        MULTI_OUT_SAME = 2

    TX_SUBTYPE_CHOICES = (
        (TxSubtype.MULTI_OUT, _("MultiOut Payment")),
        (TxSubtype.MULTI_OUT_SAME, _("MultiOutSame Payment")),
    )

    id = models.BigAutoField(primary_key=True)
    height = models.IntegerField()
    tx_id = PositiveBigIntegerField()
    sender_id = PositiveBigIntegerField(db_index=True)
    recipient_id = PositiveBigIntegerField(db_index=True)
    amount = PositiveBigIntegerField()
    tx_subtype = models.PositiveSmallIntegerField(choices=TX_SUBTYPE_CHOICES)
    tx_timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = ["height", "tx_timestamp"]
        unique_together = ["tx_id", "recipient_id"]
