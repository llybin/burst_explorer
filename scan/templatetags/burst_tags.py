from datetime import datetime, timedelta
from math import ceil

from django import template

from burst.constants import MAX_BASE_TARGET
from burst.libs.reed_solomon import ReedSolomon
from burst.libs.transactions import get_message
from java_wallet.fields import get_desc_tx_type
from java_wallet.models import Block, Transaction
from scan.helpers.exchange import get_cached_exchange_data

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
    data = get_cached_exchange_data()
    return value * data.price_usd


@register.filter
def rounding(value: float, accuracy: int) -> float:
    return round(value, accuracy)


@register.filter
def bin2hex(value: bytes) -> str:
    if not value:
        return ""
    return value.hex().upper()


@register.filter
def tx_message(tx: Transaction) -> str:
    if not tx.has_message:
        return ""
    return get_message(tx.attachment_bytes)


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
    return MAX_BASE_TARGET / base_target


@register.simple_tag(takes_context=True)
def rank_row(context: dict, number: int) -> int:
    start = 0
    if context["page_obj"].number > 0:
        start = context["paginator"].per_page * (context["page_obj"].number - 1)

    return number + start


@register.filter
def tx_deadline(value):
    return value["timestamp"] + timedelta(minutes=value["deadline"]) - datetime.now()


@register.filter()
def smooth_timedelta(timedelta_obj):
    secs = timedelta_obj.total_seconds()
    time_str = ""
    if secs > 86400:  # 60sec * 60min * 24hrs
        days = secs // 86400
        time_str += f"{int(days)} d"
        secs = secs - days * 86400

    if secs > 3600:
        hours = secs // 3600
        time_str += f" {int(hours)} h"
        secs = secs - hours * 3600

    if secs > 60:
        minutes = ceil(secs / 60)
        time_str += f" {int(minutes)} min"

    if not time_str:
        time_str = f"{int(secs)} seconds"

    return time_str
