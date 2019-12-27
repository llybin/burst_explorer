from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView

from scan.models import PeerMonitor


@require_http_methods(["GET"])
def peers_charts_view(request):
    online_now = PeerMonitor.objects.filter(state=PeerMonitor.State.ONLINE).count()
    versions = (
        PeerMonitor.objects.filter(state=PeerMonitor.State.ONLINE)
        .values("version")
        .annotate(cnt=Count("version"))
        .order_by("-cnt", "-version")
    )

    countries = (
        PeerMonitor.objects.filter(state=PeerMonitor.State.ONLINE)
        .values("country_code")
        .annotate(cnt=Count("country_code"))
        .order_by("-cnt", "country_code")
    )

    states = (
        PeerMonitor.objects.values("state")
        .annotate(cnt=Count("state"))
        .order_by("-cnt", "state")
    )
    for state in states:
        state["state"] = PeerMonitor(state=state["state"]).get_state_display()

    last_check = (
        PeerMonitor.objects.values("modified_at").order_by("-modified_at").first()
    )

    return render(
        request,
        "peers/charts.html",
        {
            "online_now": online_now,
            "versions": versions,
            "countries": countries,
            "states": states,
            "last_check": last_check,
        },
    )


class PeerMonitorListView(ListView):
    model = PeerMonitor
    queryset = PeerMonitor.objects.all()
    template_name = "peers/list.html"
    context_object_name = "peers"
    paginate_by = 25
    ordering = ("-height", "announced_address")


class PeerMonitorDetailView(DetailView):
    model = PeerMonitor
    queryset = PeerMonitor.objects.all()
    template_name = "peers/detail.html"
    context_object_name = "peer"
    slug_field = "announced_address"
    slug_url_kwarg = "address"
