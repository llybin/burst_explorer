from django.views.generic import ListView

from java_wallet.models import Block
from scan.caching_paginator import CachingPaginator
from scan.helpers.last_block import get_cached_last_height
from scan.helpers.queries import (
    get_account_name,
    get_pool_id_for_block,
    get_txs_count_in_block,
)
from scan.views.base import IntSlugDetailView
from scan.views.filters.blocks import BlockFilter


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
        return BlockFilter(self.request.GET, queryset=super().get_queryset()).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_height"] = get_cached_last_height()
        obj = context[self.context_object_name]
        for b in obj:
            fill_data_block(b)

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
