""" https://github.com/burst-apps-team/burstcoin/blob/master/src/brs/Constants.java
"""

MAX_BALANCE_BURST = 2158812800

ONE_BURST = 100000000

MAX_BALANCE_NQT = MAX_BALANCE_BURST * ONE_BURST
MAX_BASE_TARGET = 18325193796

MAX_ARBITRARY_MESSAGE_LENGTH = 1000
MAX_ENCRYPTED_MESSAGE_LENGTH = 1000

MAX_MULTI_OUT_RECIPIENTS = 64
MAX_MULTI_SAME_OUT_RECIPIENTS = 128

BLOCK_CHAIN_START_AT = 1407722400


""" https://github.com/burst-apps-team/burstcoin/blob/master/src/brs/TransactionType.java
"""


class TxType:
    PAYMENT = 0
    MESSAGING = 1
    COLORED_COINS = 2
    DIGITAL_GOODS = 3
    ACCOUNT_CONTROL = 4
    BURST_MINING = 20
    ADVANCED_PAYMENT = 21
    AUTOMATED_TRANSACTIONS = 22


class TxSubtypePayment:
    ORDINARY = 0
    MULTI_OUT = 1
    MULTI_OUT_SAME = 2


class TxSubtypeMessaging:
    ARBITRARY_MESSAGE = 0
    ALIAS_ASSIGNMENT = 1
    ACCOUNT_INFO = 5
    ALIAS_SELL = 6
    ALIAS_BUY = 7


class TxSubtypeColoredCoins:
    ASSET_ISSUANCE = 0
    ASSET_TRANSFER = 1
    ASK_ORDER_PLACEMENT = 2
    BID_ORDER_PLACEMENT = 3
    ASK_ORDER_CANCELLATION = 4
    BID_ORDER_CANCELLATION = 5


class TxSubtypeDigitalGoods:
    LISTING = 0
    DELISTING = 1
    PRICE_CHANGE = 2
    QUANTITY_CHANGE = 3
    PURCHASE = 4
    DELIVERY = 5
    FEEDBACK = 6
    REFUND = 7


class TxSubtypeAccountControl:
    EFFECTIVE_BALANCE_LEASING = 0


class TxSubtypeBurstMining:
    REWARD_RECIPIENT_ASSIGNMENT = 0


class TxSubtypeAdvancedPayment:
    ESCROW_CREATION = 0
    ESCROW_SIGN = 1
    ESCROW_RESULT = 2
    SUBSCRIPTION_SUBSCRIBE = 3
    SUBSCRIPTION_CANCEL = 4
    SUBSCRIPTION_PAYMENT = 5


class TxSubtypeAutomatedTransactions:
    CREATION = 0
    PAYMENT = 1
