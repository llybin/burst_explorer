from django.db.models import Q
from django_filters import FilterSet, NumberFilter

from java_wallet.models import Transaction


class TxFilter(FilterSet):
    block = NumberFilter(field_name="block__height")
    a = NumberFilter(method="filter_by_account")

    class Meta:
        model = Transaction
        fields = ("block", "a")

    @staticmethod
    def filter_by_account(queryset, name, value):
        return queryset.filter(Q(sender_id=value) | Q(recipient_id=value))
