from django.views.generic import ListView

from java_wallet.models import Asset, AssetTransfer, Trade
from scan.caching_paginator import CachingPaginator
from scan.helpers import get_account_name, get_asset_details
from scan.views.base import IntSlugDetailView


class AssetListView(ListView):
    model = Asset
    queryset = Asset.objects.using('java_wallet').all()
    template_name = 'assets/list.html'
    context_object_name = 'assets'
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = '-height'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            t.account_name = get_account_name(t.account_id)

        return context


class AssetDetailView(IntSlugDetailView):
    model = Asset
    queryset = Asset.objects.using('java_wallet').all()
    template_name = 'assets/detail.html'
    context_object_name = 'asset'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        context['account_name'] = get_account_name(obj.account_id)

        # assets transfer

        context['assets_transfers'] = AssetTransfer.objects.using('java_wallet').using('java_wallet').filter(
            asset_id=obj.id
        ).order_by('-height')[:15]

        for asset in context['assets_transfers']:
            asset.name, asset.decimals, asset.total_quantity = get_asset_details(asset.asset_id)

            asset.sender_name = get_account_name(asset.sender_id)
            asset.recipient_name = get_account_name(asset.recipient_id)

        context['assets_transfers_cnt'] = AssetTransfer.objects.using('java_wallet').filter(
            asset_id=obj.id
        ).count()

        # assets trades

        context['assets_trades'] = Trade.objects.using('java_wallet').using('java_wallet').filter(
            asset_id=obj.id
        ).order_by('-height')[:15]

        for asset in context['assets_trades']:
            asset.name, asset.decimals, asset.total_quantity = get_asset_details(asset.asset_id)

            asset.buyer_name = get_account_name(asset.buyer_id)
            asset.seller_name = get_account_name(asset.seller_id)

        context['assets_trades_cnt'] = Trade.objects.using('java_wallet').filter(
            asset_id=obj.id
        ).count()

        return context
