from django import template

from scan.models import PeerMonitor

register = template.Library()


@register.filter
def availability(node: PeerMonitor) -> float:
    return 100 - (node.downtime / node.lifetime) * 100
