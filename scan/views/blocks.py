from django.views.generic import ListView

from java_wallet.models import Block
from scan.caching_paginator import CachingPaginator
from scan.helpers import get_txs_count_in_block, get_account_name, get_pool_id_for_block, get_last_height
from scan.views.base import IntSlugDetailView


class BlockListView(ListView):
    model = Block
    queryset = Block.objects.using('java_wallet').all()
    template_name = 'blocks/list.html'
    context_object_name = 'blocks'
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = '-height'

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET.get('m'):
            qs = qs.filter(generator_id=self.request.GET.get('m'))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for b in obj:
            b.txs_cnt = get_txs_count_in_block(b.id)

            b.generator_name = get_account_name(b.generator_id)

            pool_id = get_pool_id_for_block(b)
            if pool_id:
                b.pool_id = pool_id
                b.pool_name = get_account_name(pool_id)

        context['last_height'] = get_last_height()

        return context


class BlockDetailView(IntSlugDetailView):
    model = Block
    queryset = Block.objects.using('java_wallet').all()
    template_name = 'blocks/detail.html'
    context_object_name = 'blk'
    slug_field = 'height'
    slug_url_kwarg = 'height'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        context['txs_cnt'] = get_txs_count_in_block(obj.id)
        context['generator_name'] = get_account_name(obj.generator_id)

        pool_id = get_pool_id_for_block(obj)
        if pool_id:
            context['pool_id'] = pool_id
            context['pool_name'] = get_account_name(pool_id)

        return context
