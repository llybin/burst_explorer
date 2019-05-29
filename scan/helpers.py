from django.core.cache import cache

from java_wallet.models import Account, Transaction


def get_account_name(account_id):
    key = "account_name_{}".format(account_id)

    account_name = cache.get(key)

    if not account_name:
        account_name = Account.objects.using('java-wallet').filter(
            id=account_id, latest=True
        ).values_list(
            'name', flat=True
        ).first()
        cache.set(key, account_name)

    return account_name


def get_txs_count_in_block(block_id):
    key = "block_txs_count_{}".format(block_id)

    cnt = cache.get(key)

    if not cnt:
        cnt = Transaction.objects.using('java-wallet').filter(block_id=block_id).count()
        cache.set(key, cnt)

    return cnt
