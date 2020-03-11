from django.db.models import Q
from django.views.generic import ListView

from burst.libs.multiout import MultiOutPack
from java_wallet.models import Transaction
from scan.caching_paginator import CachingPaginator
from scan.helpers.queries import get_account_name, get_last_height, get_txs_count
from scan.models import MultiOut
from scan.views.base import IntSlugDetailView


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

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET.get("block"):
            qs = qs.filter(block__height=self.request.GET.get("block"))

        elif self.request.GET.get("a"):
            qs = qs.filter(
                Q(sender_id=self.request.GET.get("a"))
                | Q(recipient_id=self.request.GET.get("a"))
            )

        else:
            qs = qs[:100000]

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            fill_data_transaction(t, list_page=True)

        # TODO: needed only if no filtering
        context["txs_cnt"] = get_txs_count()

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
