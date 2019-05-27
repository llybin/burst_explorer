import logging

from django.utils.translation import ugettext as _


TX_TYPES = {
    (0, 0): _("Ordinary Payment"),
    (0, 1): _("Multiout Payment"),
    (0, 2): _("Multiout Payment"),
    (1, 0): _("Arbitrary Message"),
    (1, 1): _("Alias Assignment"),
    (1, 5): _("Account Update"),
    (1, 6): _("Alias sell"),
    (1, 7): _("Alias buy"),
    (2, 0): _("Asset issuance"),
    (2, 1): _("Asset Transfer"),
    (2, 2): _("Ask Order Placement"),
    (2, 3): _("Bid Order Placement"),
    (2, 4): _("Ask order cancellation"),
    (2, 5): _("Bid order cancellation"),
    (3, 0): _("Marketplace Listing"),
    (3, 1): _("Marketplace Removal"),
    (3, 2): _("Marketplace Price Change"),
    (3, 3): _("Quantity change"),
    (3, 4): _("Marketplace Purchase"),
    (3, 5): _("Marketplace Delivery"),
    (3, 6): _("Marketplace Feedback"),
    (3, 7): _("Marketplace Refund"),
    (4, 0): _("Effective balance leasing"),
    (20, 0): _("Reward Assignment"),
    (21, 3): _("Subscription Subscribe"),
    (21, 5): _("Subscription Payment"),
    (22, 0): _("AT Creation"),
}


def get_desc_tx_type(tx_type, tx_subtype):
    if (tx_type, tx_subtype) in TX_TYPES:
        return TX_TYPES[(tx_type, tx_subtype)]

    else:
        logging.warning("Unknown transaction type: %d-%d", tx_type, tx_subtype)
        return _("Unknown type")
