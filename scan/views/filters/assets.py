from django.db.models import Q
from django_filters import FilterSet, NumberFilter

from java_wallet.models import AssetTransfer, Trade


class TradeFilter(FilterSet):
    asset = NumberFilter(field_name="asset_id")
    a = NumberFilter(method="filter_by_account")

    class Meta:
        model = Trade
        fields = ("asset", "a")

    @staticmethod
    def filter_by_account(queryset, name, value):
        return queryset.filter(Q(buyer_id=value) | Q(seller_id=value))


class AssetTransferFilter(FilterSet):
    asset = NumberFilter(field_name="asset_id")
    a = NumberFilter(method="filter_by_account")

    class Meta:
        model = AssetTransfer
        fields = ("asset", "a")

    @staticmethod
    def filter_by_account(queryset, name, value):
        return queryset.filter(Q(sender_id=value) | Q(recipient_id=value))
