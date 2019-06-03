from django.db.models import Q
from django.views.generic import ListView

from burst.multiout import MultiOutPack
from java_wallet.models import Account, Transaction, AccountAsset, AssetTransfer, Trade, Block
from scan.caching_paginator import CachingPaginator
from scan.helpers import get_all_burst_amount, get_account_name, get_asset_details, get_pool_id_for_account
from scan.models import MultiOut
from scan.views.base import IntSlugDetailView


class AccountsListView(ListView):
    model = Account
    queryset = Account.objects.using('java_wallet').filter(latest=True).all()
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = '-balance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['balance__sum'] = get_all_burst_amount()

        return context


class AddressDetailView(IntSlugDetailView):
    model = Account
    queryset = Account.objects.using('java_wallet').filter(latest=True).all()
    template_name = 'accounts/detail.html'
    context_object_name = 'address'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        # transactions

        context['txs'] = Transaction.objects.using('java_wallet').filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
        ).order_by('-height')[:15]

        for t in context['txs']:
            t.sender_name = get_account_name(t.sender_id)
            if t.recipient_id:
                t.recipient_name = get_account_name(t.recipient_id)

            if t.type == 0 and t.subtype in {1, 2}:
                v, t.multiout = MultiOutPack().unpack_header(t.attachment_bytes)

        context['txs_cnt'] = Transaction.objects.using('java_wallet').filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
        ).count()

        # multiouts

        context['mos'] = MultiOut.objects.filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
        ).order_by('-height')[:15]

        for t in context['mos']:
            t.sender_name = get_account_name(t.sender_id)
            if t.recipient_id:
                t.recipient_name = get_account_name(t.recipient_id)

        context['mos_cnt'] = MultiOut.objects.filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
        ).count()

        # assets

        context['assets'] = AccountAsset.objects.using('java_wallet').filter(
            account_id=obj.id,
            latest=True
        ).order_by('-db_id')

        for asset in context['assets']:
            asset.name, asset.decimals, asset.total_quantity = get_asset_details(asset.asset_id)

        context['assets_cnt'] = AccountAsset.objects.using('java_wallet').filter(
            account_id=obj.id,
            latest=True
        ).count()

        # assets transfer

        context['assets_transfers'] = AssetTransfer.objects.using('java_wallet').using('java_wallet').filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
        ).order_by('-height')[:15]

        for asset in context['assets_transfers']:
            asset.name, asset.decimals, asset.total_quantity = get_asset_details(asset.asset_id)

            asset.sender_name = get_account_name(asset.sender_id)
            asset.recipient_name = get_account_name(asset.recipient_id)

        context['assets_transfers_cnt'] = AssetTransfer.objects.using('java_wallet').filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
        ).count()

        # assets trades

        context['assets_trades'] = Trade.objects.using('java_wallet').using('java_wallet').filter(
            Q(buyer_id=obj.id) | Q(seller_id=obj.id)
        ).order_by('-height')[:15]

        for asset in context['assets_trades']:
            asset.name, asset.decimals, asset.total_quantity = get_asset_details(asset.asset_id)

            asset.buyer_name = get_account_name(asset.buyer_id)
            asset.seller_name = get_account_name(asset.seller_id)

        context['assets_trades_cnt'] = Trade.objects.using('java_wallet').filter(
            Q(buyer_id=obj.id) | Q(seller_id=obj.id)
        ).count()

        # pool info

        pool_id = get_pool_id_for_account(obj.id)
        if pool_id:
            context['pool_id'] = pool_id
            context['pool_name'] = get_account_name(pool_id)

        # blocks

        context['mined_blocks'] = Block.objects.using('java_wallet').filter(
            generator_id=obj.id
        ).order_by('-height')[:15]

        context['mined_blocks_cnt'] = Block.objects.using('java_wallet').filter(
            generator_id=obj.id
        ).count()

        return context
