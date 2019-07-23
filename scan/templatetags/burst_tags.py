from datetime import timedelta

from django import template

from burst.libs.reed_solomon import ReedSolomon
from java_wallet.fields import get_desc_tx_type
from java_wallet.models import Block, Transaction
from scan.helpers import get_exchange_info

register = template.Library()


def get_block_reward(block: Block) -> int:
    month = int(block.height / 10800)
    return int(pow(0.95, month) * 10000)


@register.filter
def block_reward(block: Block) -> int:
    return get_block_reward(block)


@register.filter
def block_reward_fee(block: Block) -> float:
    return get_block_reward(block) + block.total_fee / 10 ** 8


@register.filter
def burst_amount(value: int) -> float:
    return value / 10 ** 8


@register.filter
def in_usd(value: float) -> float:
    info = get_exchange_info()
    return value * info['price_usd']


@register.filter
def rounding(value: float, accuracy: int) -> float:
    return round(value, accuracy)


@register.filter
def bin2hex(value: bytes) -> str:
    if not value:
        return ''
    return value.hex().upper()


@register.filter
def tx_type(tx: Transaction) -> str:
    return get_desc_tx_type(tx.type, tx.subtype)


@register.filter
def num2rs(value: str or int) -> str:
    return ReedSolomon().encode(str(value))


@register.simple_tag()
def block_generation_time(block: Block) -> timedelta:
    if block.previous_block:
        return block.timestamp - block.previous_block.timestamp
    else:
        # first block
        return timedelta(0)


@register.filter
def sub(a: int or float, b: int or float) -> int or float:
    return a - b


@register.filter
def div(a: int or float, b: int or float) -> float:
    return a / b


@register.filter
def mul(a: int or float, b: int or float) -> int or float:
    return a * b


@register.filter
def div_decimals(a: int or float, b: int) -> float:
    return a / 10 ** b


@register.filter
def mul_decimals(a: int or float, b: int) -> float:
    return a * 10 ** b


@register.filter
def percent(value: int or float, total: int or float) -> int or float:
    return value / total * 100


@register.filter
def net_diff(base_target: int) -> float:
    return 18325193796. / base_target


@register.simple_tag(takes_context=True)
def rank_row(context: dict, number: int) -> int:
    start = 0
    if context['page_obj'].number > 0:
        start = context['paginator'].per_page * (context['page_obj'].number - 1)

    return number + start
