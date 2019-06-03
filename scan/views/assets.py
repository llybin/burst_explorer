from django.views.generic import ListView

from java_wallet.models import Asset, AssetTransfer, Trade
from scan.caching_paginator import CachingPaginator
from scan.helpers import get_account_name, get_asset_details
from scan.views.base import IntSlugDetailView


def fill_data_asset_transfer(transfer):
    transfer.name, transfer.decimals, transfer.total_quantity = get_asset_details(transfer.asset_id)

    transfer.sender_name = get_account_name(transfer.sender_id)
    transfer.recipient_name = get_account_name(transfer.recipient_id)


def fill_data_asset_trade(trade):
    trade.name, trade.decimals, trade.total_quantity = get_asset_details(trade.asset_id)

    trade.buyer_name = get_account_name(trade.buyer_id)
    trade.seller_name = get_account_name(trade.seller_id)


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

        obj.account_name = get_account_name(obj.account_id)

        # assets transfer

        assets_transfers = AssetTransfer.objects.using('java_wallet').using('java_wallet').filter(
            asset_id=obj.id
        ).order_by('-height')[:15]

        for transfer in assets_transfers:
            fill_data_asset_transfer(transfer)

        context['assets_transfers'] = assets_transfers

        context['assets_transfers_cnt'] = AssetTransfer.objects.using('java_wallet').filter(
            asset_id=obj.id
        ).count()

        # assets trades

        assets_trades = Trade.objects.using('java_wallet').using('java_wallet').filter(
            asset_id=obj.id
        ).order_by('-height')[:15]

        for trade in assets_trades:
            fill_data_asset_trade(trade)

        context['assets_trades'] = assets_trades

        context['assets_trades_cnt'] = Trade.objects.using('java_wallet').filter(
            asset_id=obj.id
        ).count()

        return context
