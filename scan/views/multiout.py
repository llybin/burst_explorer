from django.db.models import Q
from django.views.generic import ListView

from scan.caching_paginator import CachingPaginator
from scan.helpers import get_account_name, get_multiouts_count
from scan.models import MultiOut


def fill_data_multiouts(obj):
    obj.sender_name = get_account_name(obj.sender_id)
    if obj.recipient_id:
        obj.recipient_name = get_account_name(obj.recipient_id)


class MultiOutListView(ListView):
    model = MultiOut
    queryset = MultiOut.objects.all()
    template_name = 'mos/list.html'
    context_object_name = 'mos'
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = '-height'

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.GET.get('block'):
            qs = qs.filter(height=self.request.GET.get('block'))

        elif self.request.GET.get('a'):
            qs = qs.filter(
                Q(sender_id=self.request.GET.get('a')) | Q(recipient_id=self.request.GET.get('a'))
            )

        else:
            qs = qs[:100000]

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj = context[self.context_object_name]

        for t in obj:
            fill_data_multiouts(t)

        context['mos_cnt'] = get_multiouts_count()

        return context
