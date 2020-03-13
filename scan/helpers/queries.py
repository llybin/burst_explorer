from cache_memoize import cache_memoize

from java_wallet.models import Account, Asset, Block, RewardRecipAssign, Transaction


@cache_memoize(86400)
def get_account_name(account_id: int) -> str:
    return (
        Account.objects.using("java_wallet")
        .filter(id=account_id, latest=True)
        .values_list("name", flat=True)
        .first()
    )


@cache_memoize(None)
def get_asset_details(asset_id: int) -> (str, int, int):
    asset_details = (
        Asset.objects.using("java_wallet")
        .filter(id=asset_id)
        .values_list("name", "decimals", "quantity")
        .first()
    )

    # BurstScan
    if asset_id == 14686983107863035136:
        asset_details = (
            f"{asset_details[0]} ❤️",
            asset_details[1],
            asset_details[2],
        )

    return asset_details


@cache_memoize(None)
def get_txs_count_in_block(block_id: int) -> int:
    return Transaction.objects.using("java_wallet").filter(block_id=block_id).count()


@cache_memoize(None)
def get_pool_id_for_block(block: Block) -> int:
    return (
        Transaction.objects.using("java_wallet")
        .filter(type=20, height__lte=block.height, sender_id=block.generator_id)
        .values_list("recipient_id", flat=True)
        .order_by("-height")
        .first()
    )


@cache_memoize(3600)
def get_pool_id_for_account(address_id: int) -> int:
    return (
        RewardRecipAssign.objects.using("java_wallet")
        .filter(account_id=address_id)
        .values_list("recip_id", flat=True)
        .order_by("-height")
        .first()
    )
