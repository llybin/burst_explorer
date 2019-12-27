from django.utils.translation import ugettext as _

from burst.constants import (
    TxSubtypeAccountControl,
    TxSubtypeAdvancedPayment,
    TxSubtypeAutomatedTransactions,
    TxSubtypeBurstMining,
    TxSubtypeColoredCoins,
    TxSubtypeDigitalGoods,
    TxSubtypeMessaging,
    TxSubtypePayment,
    TxType,
)

TX_TYPES = {
    (TxType.PAYMENT, TxSubtypePayment.ORDINARY): _("Ordinary Payment"),
    (TxType.PAYMENT, TxSubtypePayment.MULTI_OUT): _("MultiOut Payment"),
    (TxType.PAYMENT, TxSubtypePayment.MULTI_OUT_SAME): _("MultiOutSame Payment"),
    (TxType.MESSAGING, TxSubtypeMessaging.ARBITRARY_MESSAGE): _("Arbitrary Message"),
    (TxType.MESSAGING, TxSubtypeMessaging.ALIAS_ASSIGNMENT): _("Alias Assignment"),
    (TxType.MESSAGING, TxSubtypeMessaging.ACCOUNT_INFO): _("Account Update"),
    (TxType.MESSAGING, TxSubtypeMessaging.ALIAS_SELL): _("Alias Sell"),
    (TxType.MESSAGING, TxSubtypeMessaging.ALIAS_BUY): _("Alias Buy"),
    (TxType.COLORED_COINS, TxSubtypeColoredCoins.ASSET_ISSUANCE): _("Asset Issuance"),
    (TxType.COLORED_COINS, TxSubtypeColoredCoins.ASSET_TRANSFER): _("Asset Transfer"),
    (TxType.COLORED_COINS, TxSubtypeColoredCoins.ASK_ORDER_PLACEMENT): _(
        "Ask Order Placement"
    ),
    (TxType.COLORED_COINS, TxSubtypeColoredCoins.BID_ORDER_PLACEMENT): _(
        "Bid Order Placement"
    ),
    (TxType.COLORED_COINS, TxSubtypeColoredCoins.ASK_ORDER_CANCELLATION): _(
        "Ask Order Cancellation"
    ),
    (TxType.COLORED_COINS, TxSubtypeColoredCoins.BID_ORDER_CANCELLATION): _(
        "Bid Order Cancellation"
    ),
    (TxType.DIGITAL_GOODS, TxSubtypeDigitalGoods.LISTING): _("Marketplace Listing"),
    (TxType.DIGITAL_GOODS, TxSubtypeDigitalGoods.DELISTING): _("Marketplace Removal"),
    (TxType.DIGITAL_GOODS, TxSubtypeDigitalGoods.PRICE_CHANGE): _(
        "Marketplace Price Change"
    ),
    (TxType.DIGITAL_GOODS, TxSubtypeDigitalGoods.QUANTITY_CHANGE): _("Quantity Change"),
    (TxType.DIGITAL_GOODS, TxSubtypeDigitalGoods.PURCHASE): _("Marketplace Purchase"),
    (TxType.DIGITAL_GOODS, TxSubtypeDigitalGoods.DELIVERY): _("Marketplace Delivery"),
    (TxType.DIGITAL_GOODS, TxSubtypeDigitalGoods.FEEDBACK): _("Marketplace Feedback"),
    (TxType.DIGITAL_GOODS, TxSubtypeDigitalGoods.REFUND): _("Marketplace Refund"),
    (TxType.ACCOUNT_CONTROL, TxSubtypeAccountControl.EFFECTIVE_BALANCE_LEASING): _(
        "Balance Leasing"
    ),
    (TxType.BURST_MINING, TxSubtypeBurstMining.REWARD_RECIPIENT_ASSIGNMENT): _(
        "Reward Recipient Assignment"
    ),
    (TxType.ADVANCED_PAYMENT, TxSubtypeAdvancedPayment.ESCROW_CREATION): _(
        "Escrow Creation"
    ),
    (TxType.ADVANCED_PAYMENT, TxSubtypeAdvancedPayment.ESCROW_SIGN): _("Escrow Sign"),
    (TxType.ADVANCED_PAYMENT, TxSubtypeAdvancedPayment.ESCROW_RESULT): _(
        "Escrow Result"
    ),
    (TxType.ADVANCED_PAYMENT, TxSubtypeAdvancedPayment.SUBSCRIPTION_SUBSCRIBE): _(
        "Subscription Subscribe"
    ),
    (TxType.ADVANCED_PAYMENT, TxSubtypeAdvancedPayment.SUBSCRIPTION_CANCEL): _(
        "Subscription Cancel"
    ),
    (TxType.ADVANCED_PAYMENT, TxSubtypeAdvancedPayment.SUBSCRIPTION_PAYMENT): _(
        "Subscription Payment"
    ),
    (TxType.AUTOMATED_TRANSACTIONS, TxSubtypeAutomatedTransactions.CREATION): _(
        "AT Creation"
    ),
    (TxType.AUTOMATED_TRANSACTIONS, TxSubtypeAutomatedTransactions.PAYMENT): _(
        "AT Payment"
    ),
}
