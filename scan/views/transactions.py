from django.http import Http404
from django.views.generic import ListView

from burst.libs.multiout import MultiOutPack
from java_wallet.models import Transaction
from scan.caching_data.last_height import CachingLastHeight
from scan.caching_data.pending_txs import CachingPendingTxs
from scan.caching_data.total_txs_count import CachingTotalTxsCount
from scan.caching_paginator import CachingPaginator
from scan.helpers.queries import get_account_name
from scan.models import MultiOut
from scan.views.base import IntSlugDetailView
from scan.views.filters.transactions import TxFilter


def fill_data_transaction(obj, list_page=True):
    obj.sender_name = get_account_name(obj.sender_id)
    if obj.recipient_id:
        obj.recipient_name = get_account_name(obj.recipient_id)

    if obj.type == 0 and obj.subtype in {1, 2}:
        if obj.height == 0:
            # TODO: quick hack pending transaction
            return
        v, obj.multiout = MultiOutPack().unpack_header(obj.attachment_bytes)
        if not list_page:
            obj.recipients = MultiOut.objects.filter(tx_id=obj.id).all()


class TxListView(ListView):
    model = Transaction
    queryset = Transaction.objects.using("java_wallet").all()
    template_name = "txs/list.html"
    context_object_name = "txs"
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = ("-height", "-timestamp")
    filter_set = None

    def get_queryset(self):
        self.filter_set = TxFilter(self.request.GET, queryset=super().get_queryset())
        qs = self.filter_set.qs
        if not self.filter_set.data:
            qs = qs[:100000]

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context[self.context_object_name]
        for t in obj:
            fill_data_transaction(t, list_page=True)

        # if no filtering get cached total count instead paginator.count in template
        if not self.filter_set.data:
            context["txs_cnt"] = CachingTotalTxsCount().cached_data

        return context


class TxDetailView(IntSlugDetailView):
    model = Transaction
    queryset = Transaction.objects.using("java_wallet").all()
    template_name = "txs/detail.html"
    context_object_name = "tx"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_object(self, queryset=None):
        try:
            obj = super().get_object(queryset)
        except Http404 as e:
            txs_pending = list(
                filter(
                    lambda x: x.get("transaction")
                    == self.kwargs.get(self.slug_url_kwarg),
                    CachingPendingTxs().cached_data,
                )
            )
            if not txs_pending:
                raise e

            tx = txs_pending[0]
            obj = Transaction(
                id=int(tx["transaction"]),
                deadline=tx["deadline"],
                sender_public_key=tx["senderPublicKey"].encode(),
                recipient_id=tx.get("recipient"),
                amount=tx["amountNQT"],
                fee=tx["feeNQT"],
                height=0,  # TODO why tx["height"] exists?
                block_id=0,
                signature=tx["signature"].encode(),
                timestamp=tx["timestamp"],
                type=tx["type"],
                subtype=tx["subtype"],
                sender_id=int(tx["sender"]),
                block_timestamp=tx["timestamp"],  # TODO
                full_hash=tx["fullHash"].encode(),
                referenced_transaction_fullhash=None,  # TODO
                attachment_bytes=None,  # TODO: 'attachment': {'version.MultiSameOutCreation': 1, 'recipients': [820256820168033388, 8087908814943479341]}
                version=tx["version"],
                has_message=False,  # TODO 'attachment': {'version.Message': 1, 'message': 'test', 'messageIsText': True}
                has_encrypted_message=False,  # TODO 'attachment': {'version.EncryptedMessage': 1, 'encryptedMessage': {'data': '952f0ff3bff6b61dbf4bd3677598e81dc114c1f0d3000d6fd2dd522f4cfa9e5e0fa836f15d668c60ab1d1aea9d4b4a2434c21d8116a0812ddb2d4b04431a330c', 'nonce': 'da9ace93c11ea07f584a56c74964166a0209ffbb3f4fc14c7a92aa71ac663444', 'isText': True}}
                has_public_key_announcement=False,  # TODO
                ec_block_height=tx["ecBlockHeight"],
                ec_block_id=tx["ecBlockId"],
                has_encrypttoself_message=False,  # TODO
            )
            obj.attachment = tx.get("attachment")
            obj.multiout = tx.get("multiout")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context[self.context_object_name]
        obj.blocks_confirm = CachingLastHeight().cached_data - obj.height
        fill_data_transaction(obj, list_page=False)
        return context
