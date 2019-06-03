from django.shortcuts import render

from java_wallet.models import Transaction, Block
from scan.helpers import get_last_height, get_account_name, get_txs_count_in_block, get_pool_id_for_block
from burst.multiout import MultiOutPack


def index(request):
    txs = Transaction.objects.using('java_wallet').order_by('-height')[:5]

    for t in txs:
        t.sender_name = get_account_name(t.sender_id)
        if t.recipient_id:
            t.recipient_name = get_account_name(t.recipient_id)

        if t.type == 0 and t.subtype in {1, 2}:
            v, t.multiout = MultiOutPack().unpack_header(t.attachment_bytes)

    blocks = Block.objects.using('java_wallet').order_by('-height')[:5]

    for b in blocks:
        b.txs_cnt = get_txs_count_in_block(b.id)

        b.generator_name = get_account_name(b.generator_id)

        pool_id = get_pool_id_for_block(b)
        if pool_id:
            b.pool_id = pool_id
            b.pool_name = get_account_name(pool_id)

    context = {
        'last_height': get_last_height(),
        'txs': txs,
        'blocks': blocks,
    }

    return render(request, 'home/index.html', context)
