from django.db.models import Count
from django.views.generic import ListView

from scan.models import PeerMonitor


class PeerMonitorListView(ListView):
    model = PeerMonitor
    queryset = PeerMonitor.objects.all()
    template_name = 'network/nodes.html'
    context_object_name = 'nodes'
    paginate_by = 25
    ordering = ('downtime', 'address')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['online_now'] = PeerMonitor.objects.filter(proofs_online__gte=1).count()
        context['versions'] = PeerMonitor.objects.filter(
            proofs_online__gte=1
        ).values('version').annotate(cnt=Count('version')).order_by('-cnt')

        context['countries'] = PeerMonitor.objects.filter(
            proofs_online__gte=1
        ).values('country_code').annotate(cnt=Count('country_code')).order_by('-cnt')

        context['last_check'] = PeerMonitor.objects.values('modified_at').order_by('-modified_at').first()

        return context
