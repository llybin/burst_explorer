from django.db.models import Q, Sum
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from java_wallet.models import (
    Account,
    At,
    Asset,
    Block,
    Goods,
    Transaction,
)
from scan.helpers import (
    get_account_name,
    get_txs_count_in_block,
    get_pool_id_for_block,
    get_pool_id_for_account,
)


def index(request):
    return render(request, 'index.html')


class BlockListView(ListView):
    model = Block
    queryset = Block.objects.using('java-wallet').all()
    template_name = 'blocks/list.html'
    context_object_name = 'blocks'
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

        return context


class BlockDetailView(DetailView):
    model = Block
    queryset = Block.objects.using('java-wallet').all()
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


class TxListView(ListView):
    model = Transaction
    queryset = Transaction.objects.using('java-wallet').all()
    template_name = 'txs/list.html'
    context_object_name = 'txs'
    paginate_by = 25
    ordering = '-height'

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET.get('block'):
            qs = qs.filter(block__height=self.request.GET.get('block'))

        elif self.request.GET.get('a'):
            qs = qs.filter(sender_id=self.request.GET.get('a'))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            t.sender_name = get_account_name(t.sender_id)
            if t.recipient_id:
                t.recipient_name = get_account_name(t.recipient_id)

        return context


class TxDetailView(DetailView):
    model = Transaction
    queryset = Transaction.objects.using('java-wallet').all()
    template_name = 'txs/detail.html'
    context_object_name = 'tx'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        last_block = Block.objects.using('java-wallet').order_by(
            '-height'
        ).values_list(
            'height', flat=True
        ).first()

        context['blocks_confirm'] = last_block - obj.height

        context['sender_name'] = get_account_name(obj.sender_id)
        if context[self.context_object_name].recipient_id:
            context['recipient_name'] = get_account_name(obj.recipient_id)

        return context


class AccountsListView(ListView):
    model = Account
    queryset = Account.objects.using('java-wallet').filter(latest=True).all()
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'
    paginate_by = 25
    ordering = '-balance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        res = Account.objects.using('java-wallet').filter(
            latest=True
        ).aggregate(Sum('balance'))

        context['balance__sum'] = res['balance__sum']

        return context


class AddressDetailView(DetailView):
    model = Account
    queryset = Account.objects.using('java-wallet').filter(latest=True).all()
    template_name = 'accounts/detail.html'
    context_object_name = 'address'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        #

        context['txs'] = Transaction.objects.using('java-wallet').filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
        ).order_by('-height')[:15]

        for t in context['txs']:
            t.sender_name = get_account_name(t.sender_id)
            if t.recipient_id:
                t.recipient_name = get_account_name(t.recipient_id)

        context['txs_cnt'] = Transaction.objects.using('java-wallet').filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
        ).count()

        #

        pool_id = get_pool_id_for_account(obj.id)
        if pool_id:
            context['pool_id'] = pool_id
            context['pool_name'] = get_account_name(pool_id)

        #

        context['mined_blocks'] = Block.objects.using('java-wallet').filter(
            generator_id=obj.id
        ).order_by('-height')[:15]

        context['mined_blocks_cnt'] = Block.objects.using('java-wallet').filter(
            generator_id=obj.id
        ).count()

        return context


class AssetListView(ListView):
    model = Asset
    queryset = Asset.objects.using('java-wallet').all()
    template_name = 'assets/list.html'
    context_object_name = 'assets'
    paginate_by = 25
    ordering = '-height'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            t.account_name = get_account_name(t.account_id)

        return context


class AssetDetailView(DetailView):
    model = Asset
    queryset = Asset.objects.using('java-wallet').all()
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
    queryset = Goods.objects.using('java-wallet').filter(latest=True).all()
    template_name = 'marketplace/list.html'
    context_object_name = 'goods'
    paginate_by = 25
    ordering = '-height'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            t.seller_name = get_account_name(t.seller_id)

        return context


class MarketPlaceDetailView(DetailView):
    model = Goods
    queryset = Goods.objects.using('java-wallet').filter(latest=True).all()
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
    queryset = At.objects.using('java-wallet').filter(latest=True).all()
    template_name = 'ats/list.html'
    context_object_name = 'ats'
    paginate_by = 15
    ordering = '-height'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            t.creator_name = get_account_name(t.creator_id)

        return context


class AtDetailView(DetailView):
    model = At
    queryset = At.objects.using('java-wallet').filter(latest=True).all()
    template_name = 'ats/detail.html'
    context_object_name = 'at'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        context['creator_name'] = get_account_name(obj.creator_id)

        return context
