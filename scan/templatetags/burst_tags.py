import binascii

from django import template

from burst.reed_solomon import ReedSolomon
from java_wallet.constants import get_desc_tx_type

register = template.Library()


@register.simple_tag
def block_reward(block):
    month = int(block.height / 10800)
    return int(pow(0.95, month) * 10000)


@register.filter
def burst_amount(value):
    return value / 10 ** 8


@register.filter
def bin2hex(value):
    return binascii.hexlify(value).decode()


@register.filter
def tx_type(tx):
    return get_desc_tx_type(tx.type, tx.subtype)


@register.filter
def num2rs(value):
    if not value:
        return value
    return ReedSolomon().encode(str(value))


@register.simple_tag()
def block_generation_time(block):
    return block.timestamp - block.previous_block.timestamp
