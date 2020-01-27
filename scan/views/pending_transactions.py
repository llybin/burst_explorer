from django.shortcuts import render
from django.views.decorators.cache import cache_page

from scan.helpers import get_pending_txs


@cache_page(5)
def pending_transactions(request):
    context = {"txs_pending": get_pending_txs()}
    return render(request, "txs_pending/list.html", context)
