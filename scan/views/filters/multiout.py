from django.db.models import Q
from django_filters import FilterSet, NumberFilter

from scan.models import MultiOut


class MultiOutFilter(FilterSet):
    block = NumberFilter(field_name="height")
    a = NumberFilter(method="filter_by_account")

    class Meta:
        model = MultiOut
        fields = ("block", "a")

    @staticmethod
    def filter_by_account(queryset, name, value):
        return queryset.filter(Q(sender_id=value) | Q(recipient_id=value))
