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
    class State:
        ONLINE = 1
        UNREACHABLE = 2
        SYNC = 3
        STUCK = 4
        FORKED = 5

    STATE_CHOICES = (
        (State.ONLINE, _("online")),
        (State.UNREACHABLE, _("unreachable")),
        (State.SYNC, _("in sync")),
        (State.STUCK, _("stuck")),
        (State.FORKED, _("forked")),
    )

    ip = models.GenericIPAddressField(primary_key=True)
    announced_address = models.CharField(max_length=255, db_index=True)
    platform = models.CharField(max_length=255, blank=True)
    application = models.CharField(max_length=255, blank=True)
    version = models.CharField(max_length=255, blank=True)

    height = models.PositiveIntegerField(db_index=True, blank=True)
    cumulative_difficulty = models.CharField(max_length=255, blank=True)

    country_code = models.CharField(max_length=2, blank=True)
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, db_index=True)
    downtime = models.PositiveIntegerField(default=0, blank=True)
    lifetime = models.PositiveIntegerField(default=0, blank=True)
    # computed, optimization
    availability = models.FloatField(default=0, blank=True)

    last_online_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
