from django_filters import FilterSet, NumberFilter

from java_wallet.models import Block


class BlockFilter(FilterSet):
    m = NumberFilter(field_name="generator_id")

    class Meta:
        model = Block
        fields = ("m",)
