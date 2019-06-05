from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from burst.api.brs import BrsApi
from java_wallet.fields import get_desc_tx_type
from java_wallet.models import Transaction, Block
from scan.helpers import get_last_height, get_account_name
from scan.views.blocks import fill_data_block
from scan.views.transactions import fill_data_transaction


def get_pending_txs():
    # TODO: this quickly solution
    try:
        txs_pending = BrsApi(settings.BRS_NODE).get_unconfirmed_transactions()

        for t in txs_pending:
            t['timestamp'] = datetime.fromtimestamp(t['timestamp'] + 1407722400)
            t['amountNQT'] = int(t['amountNQT'])
            t['feeNQT'] = int(t['feeNQT'])
            t['sender_name'] = get_account_name(int(t['sender']))
            if 'recipient' in t:
                t['recipient_name'] = get_account_name(int(t['recipient']))
            if 'attachment' in t and 'recipients' in t['attachment']:
                t['multiout'] = len(t['attachment']['recipients'])
            t['tx_name'] = get_desc_tx_type(t['type'], t['subtype'])
            # TODO: multi recipients on hover

        txs_pending.sort(key=lambda x: x['feeNQT'], reverse=True)
    except Exception:
        txs_pending = []

    return txs_pending


# @cache_page(10)
def index(request):
    txs = Transaction.objects.using('java_wallet').order_by('-height')[:5]

    for t in txs:
        fill_data_transaction(t, list_page=True)

    blocks = Block.objects.using('java_wallet').order_by('-height')[:5]

    for b in blocks:
        fill_data_block(b)

    context = {
        'last_height': get_last_height(),
        'txs': txs,
        'blocks': blocks,
        'txs_pending': get_pending_txs(),
    }

    return render(request, 'home/index.html', context)
