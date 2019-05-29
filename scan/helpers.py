from django.core.cache import cache

from java_wallet.models import Account, Transaction, RewardRecipAssign


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


def get_pool_id_for_block(block):
    key = "block_pool_{}".format(block.id)

    recip_id = cache.get(key)

    if not recip_id:
        assign_reward_height = Transaction.objects.using('java-wallet').filter(
            type=20,
            height__lte=block.height,
            sender_id=block.generator_id
        ).values_list(
            'height', flat=True
        ).order_by('-height').first()

        if not assign_reward_height:
            cache.set(key, None)
            return None

        recip_id = RewardRecipAssign.objects.using('java-wallet').filter(
            account_id=block.generator_id, height=assign_reward_height
        ).values_list(
            'recip_id', flat=True
        ).first()

        cache.set(key, recip_id)

    return recip_id


def get_pool_id_for_account(address_id):
    key = "block_pool_{}".format(address_id)

    pool_id = cache.get(key)

    if not pool_id:
        pool_id = RewardRecipAssign.objects.using('java-wallet').filter(
            account_id=address_id
        ).values_list(
            'recip_id', flat=True
        ).order_by(
            '-height'
        ).first()

        cache.set(key, pool_id)

    return pool_id
