from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from java_wallet import models
from burst.libs.reed_solomon import ReedSolomon, ReedSolomonError
from scan.models import PeerMonitor


SEARCH_BY = [
    ('Block', 'height', '/block/{}'),
    ('Account', 'id', '/address/{}'),
    ('Asset', 'id', '/asset/{}'),
    ('Goods', 'id', '/mp/{}'),
    ('At', 'id', '/at/{}'),
    ('Transaction', 'id', '/tx/{}'),
]


@require_http_methods(["GET"])
def search_view(request):
    query = request.GET.get('q', '').strip()

    redirect_url = None

    if query.isdigit():
        query = int(query)

        for x in SEARCH_BY:
            exists = getattr(models, x[0]).objects.using('java_wallet').filter(
                **{x[1]: query}
            ).exists()

            if exists:
                redirect_url = x[2].format(query)
                break

    elif len(query) in {17, 20, 26}:
        try:
            numeric_id = ReedSolomon().decode(query)
            exists = models.Account.objects.using('java_wallet').filter(
                id=numeric_id
            ).exists()
            if exists:
                redirect_url = '/address/{}'.format(numeric_id)
        except ReedSolomonError:
            pass

    else:
        exists = PeerMonitor.objects.filter(ip=query).exists()
        if exists:
            redirect_url = '/peer/{}'.format(query)

    if redirect_url:
        return redirect(redirect_url)
    else:
        return render(request, 'base.html', {'submit': 'Search'})
