from django_filters import FilterSet, NumberFilter

from java_wallet.models import Purchase


class MarketplaceFilter(FilterSet):
    g = NumberFilter(field_name="goods_id")

    class Meta:
        model = Purchase
        fields = ("g",)
