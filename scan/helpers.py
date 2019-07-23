from datetime import datetime

import requests
from cache_memoize import cache_memoize
from django.conf import settings
from django.db.models import Sum
from requests import RequestException
from sentry_sdk import capture_exception

from burst.api.brs.v1 import BrsApi
from java_wallet.fields import get_desc_tx_type

from java_wallet.constants import TxSubtypePayment, BLOCK_CHAIN_START_AT
from java_wallet.models import Account, Transaction, RewardRecipAssign, Block, Asset
from scan.models import MultiOut


@cache_memoize(86400)
def get_account_name(account_id: int) -> str:
    return Account.objects.using('java_wallet').filter(
        id=account_id, latest=True
    ).values_list(
        'name', flat=True
    ).first()


@cache_memoize(None)
def get_asset_details(asset_id: int) -> (str, int, int):
    asset_details = Asset.objects.using('java_wallet').filter(
        id=asset_id
    ).values_list(
        'name', 'decimals', 'quantity'
    ).first()

    # BurstScan
    if asset_id == 14686983107863035136:
        asset_details = (
            '{} ❤️'.format(asset_details[0]),
            asset_details[1],
            asset_details[2],
        )

    return asset_details


@cache_memoize(None)
def get_txs_count_in_block(block_id: int) -> int:
    return Transaction.objects.using('java_wallet').filter(block_id=block_id).count()


@cache_memoize(None)
def get_pool_id_for_block(block: Block) -> int:
    return Transaction.objects.using('java_wallet').filter(
        type=20,
        height__lte=block.height,
        sender_id=block.generator_id
    ).values_list(
        'recipient_id', flat=True
    ).order_by('-height').first()


@cache_memoize(3600)
def get_pool_id_for_account(address_id: int) -> int:
    return RewardRecipAssign.objects.using('java_wallet').filter(
        account_id=address_id
    ).values_list(
        'recip_id', flat=True
    ).order_by(
        '-height'
    ).first()


@cache_memoize(86400)
def get_all_burst_amount() -> int:
    # TODO: formula?
    return Account.objects.using('java_wallet').filter(
        latest=True
    ).aggregate(Sum('balance'))['balance__sum']


@cache_memoize(3600)
def get_txs_count() -> int:
    return Transaction.objects.using('java_wallet').count()


@cache_memoize(3600)
def get_multiouts_count() -> int:
    return MultiOut.objects.count()


def get_last_height() -> int:
    return Block.objects.using('java_wallet').order_by(
        '-height'
    ).values_list(
        'height', flat=True
    ).first()


def get_pending_txs():
    try:
        txs_pending = BrsApi(settings.BRS_NODE).get_unconfirmed_transactions()

        for t in txs_pending:
            t['timestamp'] = datetime.fromtimestamp(t['timestamp'] + BLOCK_CHAIN_START_AT)
            t['amountNQT'] = int(t['amountNQT'])
            t['feeNQT'] = int(t['feeNQT'])
            t['sender_name'] = get_account_name(int(t['sender']))

            if 'recipient' in t:
                t['recipient_exists'] = Account.objects.using('java_wallet').filter(id=t['recipient']).exists()
                if t['recipient_exists']:
                    t['recipient_name'] = get_account_name(int(t['recipient']))

            if 'attachment' in t and 'recipients' in t['attachment']:
                t['multiout'] = len(t['attachment']['recipients'])

                for i, x in enumerate(t['attachment']['recipients']):
                    if t['subtype'] == TxSubtypePayment.MULTI_OUT:
                        t['attachment']['recipients'][i] = [int(x[0]), int(x[1])]
                    elif t['subtype'] == TxSubtypePayment.MULTI_OUT_SAME:
                        t['attachment']['recipients'][i] = int(x)

            t['tx_name'] = get_desc_tx_type(t['type'], t['subtype'])

        txs_pending.sort(key=lambda _x: _x['feeNQT'], reverse=True)
    except Exception as e:
        capture_exception(e)
        txs_pending = []

    return txs_pending


@cache_memoize(600)
def get_exchange_info() -> dict:
    if settings.TEST_NET:
        return {
            'price_usd': 0,
            '24h_volume_usd': 0,
            'market_cap_usd': 0,
            'percent_change_24h': 0,
        }

    try:
        response = requests.get('https://api.coinmarketcap.com/v1/ticker/burst/', timeout=1)
        response.raise_for_status()
        data = response.json()[0]
        data['price_usd'] = float(data['price_usd'])
        data['24h_volume_usd'] = float(data['24h_volume_usd'])
        data['market_cap_usd'] = float(data['market_cap_usd'])
        data['percent_change_24h'] = float(data['percent_change_24h'])
        return data
    except (RequestException, ValueError, IndexError) as e:
        capture_exception(e)
        return {
            'price_usd': 0,
            '24h_volume_usd': 0,
            'market_cap_usd': 0,
            'percent_change_24h': 0,
        }
