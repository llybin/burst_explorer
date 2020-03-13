from datetime import datetime

from django.conf import settings

from burst.api.brs.v1 import BrsApi
from burst.constants import BLOCK_CHAIN_START_AT, TxSubtypePayment
from java_wallet.fields import get_desc_tx_type
from java_wallet.models import Account
from scan.caching_data.base import CachingDataBase
from scan.helpers.queries import get_account_name


class CachingPendingTxs(CachingDataBase):
    _cache_key = "pending_txs"
    _cache_expiring = 30
    live_if_empty = True
    default_data_if_empty = []

    def _get_live_data(self):
        txs_pending = BrsApi(settings.BRS_NODE).get_unconfirmed_transactions()

        for t in txs_pending:
            t["timestamp"] = datetime.fromtimestamp(
                t["timestamp"] + BLOCK_CHAIN_START_AT
            )
            t["amountNQT"] = int(t["amountNQT"])
            t["feeNQT"] = int(t["feeNQT"])
            t["sender_name"] = get_account_name(int(t["sender"]))

            if "recipient" in t:
                t["recipient_exists"] = (
                    Account.objects.using("java_wallet")
                    .filter(id=t["recipient"])
                    .exists()
                )
                if t["recipient_exists"]:
                    t["recipient_name"] = get_account_name(int(t["recipient"]))

            if "attachment" in t and "recipients" in t["attachment"]:
                t["multiout"] = len(t["attachment"]["recipients"])

                for i, x in enumerate(t["attachment"]["recipients"]):
                    if t["subtype"] == TxSubtypePayment.MULTI_OUT:
                        t["attachment"]["recipients"][i] = [int(x[0]), int(x[1])]
                    elif t["subtype"] == TxSubtypePayment.MULTI_OUT_SAME:
                        t["attachment"]["recipients"][i] = int(x)

            t["tx_name"] = get_desc_tx_type(t["type"], t["subtype"])

        txs_pending.sort(key=lambda _x: _x["feeNQT"], reverse=True)

        return txs_pending
