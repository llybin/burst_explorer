import binascii

from django import template

from burst.reed_solomon import ReedSolomon
from java_wallet.constants import get_desc_tx_type

register = template.Library()


def get_block_reward(block):
    month = int(block.height / 10800)
    return int(pow(0.95, month) * 10000)


@register.filter
def block_reward(block):
    return get_block_reward(block)


@register.filter
def block_reward_fee(block):
    return get_block_reward(block) + block.total_fee / 10 ** 8


@register.filter
def burst_amount(value):
    return value / 10 ** 8


@register.filter
def rounding(value, accuracy):
    return round(value, accuracy)


@register.filter
def is_not_active(value):
    return "no" if value else "yes"


@register.filter
def bin2hex(value):
    if not value:
        return ''
    return binascii.hexlify(value).decode()


@register.filter
def tx_type(tx):
    return get_desc_tx_type(tx.type, tx.subtype)


@register.filter
def num2rs(value):
    if value is None:
        return value

    return ReedSolomon().encode(str(value))


@register.simple_tag()
def block_generation_time(block):
    return block.timestamp - block.previous_block.timestamp


@register.filter
def sub(value, arg):
    return value - arg


@register.filter
def boolean(value):
    return "yes" if value else "no"


@register.filter
def percent(value, total):
    return value / total * 100


@register.simple_tag(takes_context=True)
def rank_row(context, number):
    start = 0
    if context['page_obj'].number > 0:
        start = context['paginator'].per_page * (context['page_obj'].number - 1)

    return number + start
