from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from java_wallet.models import Block, Transaction, Account, Asset, Goods, At


def index(request):
    return render(request, 'index.html')


class BlockListView(ListView):
    model = Block
    queryset = Block.objects.using('java-wallet').all()
    template_name = 'blocks/list.html'
    context_object_name = 'blocks'
    paginate_by = 25
    ordering = '-height'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for b in obj:
            b.txs_cnt = Transaction.objects.using('java-wallet').filter(block_id=b.id).count()

            b.generator = Account.objects.using('java-wallet').filter(id=b.generator_id, latest=True).first()

            # _tar = Transaction.objects.using('java-wallet').filter(
            #     type=20,
            #     height__lte=b.height,
            #     sender_id=b.generator_id
            # ).order_by('-height')

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

        context['txs_cnt'] = Transaction.objects.using('java-wallet').filter(block_id=obj.id).count()
        context['generator'] = Account.objects.using('java-wallet').filter(id=obj.generator_id, latest=True).first()

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
            t.sender = Account.objects.using('java-wallet').filter(id=t.sender_id, latest=True).first()
            if t.recipient_id:
                t.recipient = Account.objects.using('java-wallet').filter(id=t.recipient_id, latest=True).first()

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

        context['sender'] = Account.objects.using('java-wallet').filter(id=obj.sender_id, latest=True).first()
        if context[self.context_object_name].recipient_id:
            context['recipient'] = Account.objects.using('java-wallet').filter(id=obj.recipient_id, latest=True).first()

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

        context['txs'] = Transaction.objects.using('java-wallet').filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
        ).order_by('-height')[:15]

        for t in context['txs']:
            t.sender = Account.objects.using('java-wallet').filter(id=t.sender_id, latest=True).first()
            if t.recipient_id:
                t.recipient = Account.objects.using('java-wallet').filter(id=t.recipient_id, latest=True).first()

        context['txs_cnt'] = Transaction.objects.using('java-wallet').filter(
            Q(sender_id=obj.id) | Q(recipient_id=obj.id)
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
            t.account = Account.objects.using('java-wallet').filter(id=t.account_id, latest=True).first()

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

        context['account'] = Account.objects.using('java-wallet').filter(id=obj.account_id, latest=True).first()

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
            t.seller = Account.objects.using('java-wallet').filter(id=t.seller_id, latest=True).first()

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

        context['seller'] = Account.objects.using('java-wallet').filter(id=obj.seller_id, latest=True).first()

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
            t.creator = Account.objects.using('java-wallet').filter(id=t.creator_id, latest=True).first()

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

        context['creator'] = Account.objects.using('java-wallet').filter(
            id=obj.creator_id, latest=True).first()

        return context
