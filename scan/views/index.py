from django.shortcuts import render
from django.views.decorators.cache import cache_page

from java_wallet.models import Block, Transaction
from scan.helpers import get_pending_txs
from scan.views.blocks import fill_data_block
from scan.views.transactions import fill_data_transaction


@cache_page(5)
def index(request):
    txs = Transaction.objects.using("java_wallet").order_by("-height")[:5]

    for t in txs:
        fill_data_transaction(t, list_page=True)

    blocks = Block.objects.using("java_wallet").order_by("-height")[:5]

    for b in blocks:
        fill_data_block(b)

    context = {"txs": txs, "blocks": blocks, "txs_pending": get_pending_txs()}

    return render(request, "home/index.html", context)
