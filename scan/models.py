from django.db.models import (
    BigAutoField,
    CharField,
    DateTimeField,
    FloatField,
    IntegerField,
    Model,
    PositiveIntegerField,
    PositiveSmallIntegerField,
)
from django.utils.translation import ugettext as _

from java_wallet.fields import PositiveBigIntegerField


class MultiOut(Model):
    class TxSubtype:
        """java_wallet/constants.py"""

        MULTI_OUT = 1
        MULTI_OUT_SAME = 2

    TX_SUBTYPE_CHOICES = (
        (TxSubtype.MULTI_OUT, _("MultiOut Payment")),
        (TxSubtype.MULTI_OUT_SAME, _("MultiOutSame Payment")),
    )

    id = BigAutoField(primary_key=True)
    height = IntegerField()
    tx_id = PositiveBigIntegerField()
    sender_id = PositiveBigIntegerField(db_index=True)
    recipient_id = PositiveBigIntegerField(db_index=True)
    amount = PositiveBigIntegerField()
    tx_subtype = PositiveSmallIntegerField(choices=TX_SUBTYPE_CHOICES)
    tx_timestamp = DateTimeField()
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        index_together = ["height", "tx_timestamp"]
        unique_together = ["tx_id", "recipient_id"]


class PeerMonitor(Model):
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

    announced_address = CharField(primary_key=True, max_length=255)
    platform = CharField(max_length=255, blank=True)
    application = CharField(max_length=255, blank=True)
    version = CharField(max_length=255, blank=True)

    height = PositiveIntegerField(db_index=True, blank=True)
    cumulative_difficulty = CharField(max_length=255, blank=True)

    country_code = CharField(max_length=2, blank=True)
    state = PositiveSmallIntegerField(choices=STATE_CHOICES, db_index=True)
    downtime = PositiveIntegerField(default=0, blank=True)
    lifetime = PositiveIntegerField(default=0, blank=True)
    # computed, optimization
    availability = FloatField(default=0, blank=True)

    last_online_at = DateTimeField()

    created_at = DateTimeField(auto_now_add=True)
    modified_at = DateTimeField(auto_now=True)
