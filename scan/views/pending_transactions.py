from django.shortcuts import render

from scan.caching_data.pending_txs import CachingPendingTxs


def pending_transactions(request):
    context = {"txs_pending": CachingPendingTxs().cached_data}
    return render(request, "txs_pending/list.html", context)
