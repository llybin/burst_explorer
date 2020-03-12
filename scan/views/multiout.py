from django.views.generic import ListView

from scan.caching_paginator import CachingPaginator
from scan.helpers.queries import get_account_name, get_multiouts_count
from scan.models import MultiOut
from scan.views.filters.multiout import MultiOutFilter


def fill_data_multiouts(obj):
    obj.sender_name = get_account_name(obj.sender_id)
    if obj.recipient_id:
        obj.recipient_name = get_account_name(obj.recipient_id)


class MultiOutListView(ListView):
    model = MultiOut
    queryset = MultiOut.objects.all()
    template_name = "mos/list.html"
    context_object_name = "mos"
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = ("-height", "-tx_timestamp")

    def get_queryset(self):
        filter_set = MultiOutFilter(self.request.GET, queryset=super().get_queryset())
        qs = filter_set.qs
        if not filter_set.data:
            qs = qs[:100000]

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mos_cnt"] = get_multiouts_count()
        obj = context[self.context_object_name]
        for t in obj:
            fill_data_multiouts(t)

        return context
