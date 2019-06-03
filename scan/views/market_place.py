from django.views.generic import ListView

from java_wallet.models import Goods, AssetTransfer
from scan.caching_paginator import CachingPaginator
from scan.helpers import get_account_name, get_asset_details
from scan.views.base import IntSlugDetailView


class MarketPlaceListView(ListView):
    model = Goods
    queryset = Goods.objects.using('java_wallet').filter(latest=True).all()
    template_name = 'marketplace/list.html'
    context_object_name = 'goods'
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = '-height'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            t.seller_name = get_account_name(t.seller_id)

        return context


class MarketPlaceDetailView(IntSlugDetailView):
    model = Goods
    queryset = Goods.objects.using('java_wallet').filter(latest=True).all()
    template_name = 'marketplace/detail.html'
    context_object_name = 'good'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        context['seller_name'] = get_account_name(obj.seller_id)

        context['purchases'] = AssetTransfer.objects.using('java_wallet').using('java_wallet').filter(
            asset_id=obj.id
        ).order_by('-height')[:15]

        for asset in context['assets_transfers']:
            asset.name, asset.decimals, asset.total_quantity = get_asset_details(asset.asset_id)

            asset.sender_name = get_account_name(asset.sender_id)
            asset.recipient_name = get_account_name(asset.recipient_id)

        context['assets_transfers_cnt'] = AssetTransfer.objects.using('java_wallet').filter(
            asset_id=obj.id
        ).count()

        return context
