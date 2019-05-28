from django.shortcuts import render
from django.views.generic import ListView, DetailView

from java_wallet.models import Block, Transaction, Account, Asset


def index(request):
    return render(request, 'index.html')


class BlockListView(ListView):
    model = Block
    queryset = Block.objects.using('java-wallet').all()
    template_name = 'blocks/list.html'
    context_object_name = 'blocks'
    paginate_by = 15
    ordering = '-height'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for b in context[self.context_object_name]:
            b.txs_cnt = Transaction.objects.using('java-wallet').filter(
                block_id=b.id).count()

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
        context['txs_cnt'] = Transaction.objects.using('java-wallet').filter(
            block_id=context[self.context_object_name].id).count()
        return context


class TxListView(ListView):
    model = Transaction
    queryset = Transaction.objects.using('java-wallet').all()
    template_name = 'txs/list.html'
    context_object_name = 'txs'
    paginate_by = 15
    ordering = '-timestamp'

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET.get('block'):
            qs = qs.filter(block__height=self.request.GET.get('block'))

        elif self.request.GET.get('a'):
            qs = qs.filter(sender_id=self.request.GET.get('a'))

        return qs


class TxDetailView(DetailView):
    model = Transaction
    queryset = Transaction.objects.using('java-wallet').all()
    template_name = 'txs/detail.html'
    context_object_name = 'tx'
    slug_field = 'id'
    slug_url_kwarg = 'id'


class AddressDetailView(DetailView):
    model = Account
    queryset = Account.objects.using('java-wallet').filter(latest=True).all()
    template_name = 'accounts/detail.html'
    context_object_name = 'address'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['txs'] = Transaction.objects.using('java-wallet').filter(
            sender_id=context[self.context_object_name].id).order_by('-timestamp')[:15]

        context['txs_cnt'] = Transaction.objects.using('java-wallet').filter(
            sender_id=context[self.context_object_name].id).count()
        return context


class AssetListView(ListView):
    model = Asset
    queryset = Asset.objects.using('java-wallet').all()
    template_name = 'assets/list.html'
    context_object_name = 'assets'
    paginate_by = 15
    ordering = '-id'


class AssetDetailView(DetailView):
    model = Asset
    queryset = Asset.objects.using('java-wallet').all()
    template_name = 'assets/detail.html'
    context_object_name = 'asset'
    slug_field = 'id'
    slug_url_kwarg = 'id'
