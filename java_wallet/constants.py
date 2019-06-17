""" https://github.com/burst-apps-team/burstcoin/blob/master/src/brs/TransactionType.java
"""

from django.utils.translation import ugettext as _


BLOCK_CHAIN_START_AT = 1407722400


class TxType:
    PAYMENT = 0
    NONPAYMENT = 1
    ASSET = 2
    MARKETPLACE = 3
    LEASING = 4
    REWARD_RECIPIENT = 20
    SUBSCRIPTION = 21
    AT = 22


class TxSubtypePayment:
    ORDINARY = 0
    MULTI_OUT = 1
    MULTI_OUT_SAME = 2


TX_TYPES = {
    (TxType.PAYMENT, TxSubtypePayment.ORDINARY): _("Ordinary Payment"),
    (TxType.PAYMENT, TxSubtypePayment.MULTI_OUT): _("MultiOut Payment"),
    (TxType.PAYMENT, TxSubtypePayment.MULTI_OUT_SAME): _("MultiOutSame Payment"),
    (TxType.NONPAYMENT, 0): _("Arbitrary Message"),
    (TxType.NONPAYMENT, 1): _("Alias Assignment"),
    (TxType.NONPAYMENT, 5): _("Account Update"),
    (TxType.NONPAYMENT, 6): _("Alias Sell"),
    (TxType.NONPAYMENT, 7): _("Alias Buy"),
    (TxType.ASSET, 0): _("Asset Issuance"),
    (TxType.ASSET, 1): _("Asset Transfer"),
    (TxType.ASSET, 2): _("Ask Order Placement"),
    (TxType.ASSET, 3): _("Bid Order Placement"),
    (TxType.ASSET, 4): _("Ask Order Cancellation"),
    (TxType.ASSET, 5): _("Bid Order Cancellation"),
    (TxType.MARKETPLACE, 0): _("Marketplace Listing"),
    (TxType.MARKETPLACE, 1): _("Marketplace Removal"),
    (TxType.MARKETPLACE, 2): _("Marketplace Price Change"),
    (TxType.MARKETPLACE, 3): _("Quantity Change"),
    (TxType.MARKETPLACE, 4): _("Marketplace Purchase"),
    (TxType.MARKETPLACE, 5): _("Marketplace Delivery"),
    (TxType.MARKETPLACE, 6): _("Marketplace Feedback"),
    (TxType.MARKETPLACE, 7): _("Marketplace Refund"),
    (TxType.LEASING, 0): _("Balance Leasing"),
    (TxType.REWARD_RECIPIENT, 0): _("Reward Recipient Assignment"),
    (TxType.SUBSCRIPTION, 3): _("Subscription Subscribe"),
    (TxType.SUBSCRIPTION, 5): _("Subscription Payment"),
    (TxType.AT, 0): _("AT Creation"),
}
