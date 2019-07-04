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


class PeerMonitor(models.Model):
    address = models.GenericIPAddressField(primary_key=True)
    country_code = models.CharField(max_length=2, blank=True)
    # get_peer
    announced_address = models.CharField(max_length=259, blank=True)  # 253 + len(':65535')
    platform = models.CharField(max_length=255, blank=True)
    # get_peer and get_block_chain_status
    application = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=255, blank=True)
    # get_block_chain_status
    last_block = models.CharField(max_length=20, blank=True)
    number_blocks = models.PositiveIntegerField(default=0, blank=True)
    last_blockchain_feeder = models.GenericIPAddressField(null=True, blank=True)
    last_blockchain_feeder_height = models.PositiveIntegerField(default=0, blank=True)

    proofs_online = models.PositiveIntegerField(default=0, blank=True)
    downtime = models.PositiveIntegerField(default=0, blank=True)
    lifetime = models.PositiveIntegerField(default=0, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
