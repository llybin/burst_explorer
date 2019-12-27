from django.views.generic import ListView

from java_wallet.models import Block
from scan.caching_paginator import CachingPaginator
from scan.helpers import (
    get_account_name,
    get_last_height,
    get_pool_id_for_block,
    get_txs_count_in_block,
)
from scan.views.base import IntSlugDetailView


def fill_data_block(obj):
    obj.txs_cnt = get_txs_count_in_block(obj.id)
    obj.generator_name = get_account_name(obj.generator_id)

    pool_id = get_pool_id_for_block(obj)
    if pool_id:
        obj.pool_id = pool_id
        obj.pool_name = get_account_name(pool_id)


class BlockListView(ListView):
    model = Block
    queryset = Block.objects.using("java_wallet").all()
    template_name = "blocks/list.html"
    context_object_name = "blocks"
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = "-height"

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET.get("m"):
            qs = qs.filter(generator_id=self.request.GET.get("m"))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for b in obj:
            fill_data_block(b)

        context["last_height"] = get_last_height()

        return context


class BlockDetailView(IntSlugDetailView):
    model = Block
    queryset = Block.objects.using("java_wallet").all()
    template_name = "blocks/detail.html"
    context_object_name = "blk"
    slug_field = "height"
    slug_url_kwarg = "height"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        fill_data_block(obj)

        return context
