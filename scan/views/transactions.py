from django.views.generic import ListView

from burst.libs.multiout import MultiOutPack
from java_wallet.models import Transaction
from scan.caching_paginator import CachingPaginator
from scan.helpers.queries import get_account_name, get_last_height, get_txs_total_count
from scan.models import MultiOut
from scan.views.base import IntSlugDetailView
from scan.views.filters.transactions import TxFilter


def fill_data_transaction(obj, list_page=True):
    obj.sender_name = get_account_name(obj.sender_id)
    if obj.recipient_id:
        obj.recipient_name = get_account_name(obj.recipient_id)

    if obj.type == 0 and obj.subtype in {1, 2}:
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
            context["txs_cnt"] = get_txs_total_count()

        return context


class TxDetailView(IntSlugDetailView):
    model = Transaction
    queryset = Transaction.objects.using("java_wallet").all()
    template_name = "txs/detail.html"
    context_object_name = "tx"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context[self.context_object_name]
        obj.blocks_confirm = get_last_height() - obj.height
        fill_data_transaction(obj, list_page=False)
        return context
