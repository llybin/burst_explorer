from django.db.models import Q
from django.http import Http404
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from java_wallet.models import (
    Account,
    AccountAsset,
    At,
    Asset,
    AssetTransfer,
    Trade,
    Block,
    Goods,
    Transaction,
)
from scan.helpers import (
    get_account_name,
    get_txs_count_in_block,
    get_pool_id_for_block,
    get_pool_id_for_account,
    get_all_burst_amount,
    get_txs_count,
    get_last_height,
    get_multiouts_count,
    get_asset_details,
)
from scan.caching_paginator import CachingPaginator
from burst.multiout import MultiOutPack
from scan.models import MultiOut


def index(request):
    return render(request, 'index.html')


class IntSlugDetailView(DetailView):
    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if not slug.isdigit():
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': self.queryset.model._meta.verbose_name})

        return super().get_object(queryset)


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


class MultiOutListView(ListView):
    model = MultiOut
    queryset = MultiOut.objects.all()
    template_name = 'mos/list.html'
    context_object_name = 'mos'
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = '-height'

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET.get('block'):
            qs = qs.filter(height=self.request.GET.get('block'))

        elif self.request.GET.get('a'):
            qs = qs.filter(
                Q(sender_id=self.request.GET.get('a')) | Q(recipient_id=self.request.GET.get('a'))
            )

        else:
            qs = qs[:100000]

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            t.sender_name = get_account_name(t.sender_id)
            if t.recipient_id:
                t.recipient_name = get_account_name(t.recipient_id)

        context['mos_cnt'] = get_multiouts_count()

        return context


class TxListView(ListView):
    model = Transaction
    queryset = Transaction.objects.using('java_wallet').all()
    template_name = 'txs/list.html'
    context_object_name = 'txs'
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = '-height'

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET.get('block'):
            qs = qs.filter(block__height=self.request.GET.get('block'))

        elif self.request.GET.get('a'):
            qs = qs.filter(
                Q(sender_id=self.request.GET.get('a')) | Q(recipient_id=self.request.GET.get('a'))
            )

        else:
            qs = qs[:100000]

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            t.sender_name = get_account_name(t.sender_id)
            if t.recipient_id:
                t.recipient_name = get_account_name(t.recipient_id)

            if t.type == 0 and t.subtype in {1, 2}:
                v, t.multiout = MultiOutPack().unpack_header(t.attachment_bytes)

        context['txs_cnt'] = get_txs_count()

        return context


class TxDetailView(IntSlugDetailView):
    model = Transaction
    queryset = Transaction.objects.using('java_wallet').all()
    template_name = 'txs/detail.html'
    context_object_name = 'tx'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        context['blocks_confirm'] = get_last_height() - obj.height

        context['sender_name'] = get_account_name(obj.sender_id)
        if context[self.context_object_name].recipient_id:
            context['recipient_name'] = get_account_name(obj.recipient_id)

        if obj.type == 0 and obj.subtype in {1, 2}:
            v, obj.multiout = MultiOutPack().unpack_header(obj.attachment_bytes)
            obj.recipients = MultiOut.objects.filter(tx_id=obj.id).all()

        return context


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

        context['assets_transfer'] = AssetTransfer.objects.using('java_wallet').using('java_wallet').filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
        ).order_by('-height')[:15]

        for asset in context['assets_transfer']:
            asset.name, asset.decimals, asset.total_quantity = get_asset_details(asset.asset_id)

            asset.sender_name = get_account_name(asset.sender_id)
            asset.recipient_name = get_account_name(asset.recipient_id)

        context['assets_transfer_cnt'] = AssetTransfer.objects.using('java_wallet').filter(
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

        return context


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

        return context


class AtListView(ListView):
    model = At
    queryset = At.objects.using('java_wallet').filter(latest=True).all()
    template_name = 'ats/list.html'
    context_object_name = 'ats'
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = '-height'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            t.creator_name = get_account_name(t.creator_id)

        return context


class AtDetailView(IntSlugDetailView):
    model = At
    queryset = At.objects.using('java_wallet').filter(latest=True).all()
    template_name = 'ats/detail.html'
    context_object_name = 'at'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        context['creator_name'] = get_account_name(obj.creator_id)

        return context
