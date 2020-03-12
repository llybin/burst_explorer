from django.http import Http404
from django.views.generic import ListView

from java_wallet.models import Goods, Purchase
from scan.caching_paginator import CachingPaginator
from scan.helpers.queries import get_account_name
from scan.views.base import IntSlugDetailView
from scan.views.filters.marketplace import MarketplaceFilter


class MarketPlaceListView(ListView):
    model = Goods
    queryset = Goods.objects.using("java_wallet").filter(latest=True).all()
    template_name = "marketplace/list.html"
    context_object_name = "goods"
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = "-height"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context[self.context_object_name]
        for t in obj:
            t.seller_name = get_account_name(t.seller_id)

        return context


class MarketPlacePurchasesListView(ListView):
    model = Purchase
    queryset = Purchase.objects.using("java_wallet").all()
    template_name = "marketplace/purchases.html"
    context_object_name = "purchases"
    paginator_class = CachingPaginator
    paginate_by = 25
    ordering = "-height"
    filter_set = None

    def get_queryset(self):
        self.filter_set = MarketplaceFilter(
            self.request.GET, queryset=super().get_queryset()
        )
        if self.filter_set.is_valid() and self.filter_set.data:
            qs = self.filter_set.qs[:100000]
        else:
            raise Http404()

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # total count
        context["purchases_cnt"] = self.filter_set.qs.count()
        obj = context[self.context_object_name]
        for purchase in obj:
            purchase.seller_name = get_account_name(purchase.seller_id)
            purchase.buyer_name = get_account_name(purchase.buyer_id)

        return context


class MarketPlaceDetailView(IntSlugDetailView):
    model = Goods
    queryset = Goods.objects.using("java_wallet").filter(latest=True).all()
    template_name = "marketplace/detail.html"
    context_object_name = "good"
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context[self.context_object_name]
        obj.seller_name = get_account_name(obj.seller_id)
        purchases = (
            Purchase.objects.using("java_wallet")
            .using("java_wallet")
            .filter(goods_id=obj.id)
            .order_by("-height")[:15]
        )

        for purchase in purchases:
            purchase.buyer_name = get_account_name(purchase.buyer_id)

        context["purchases"] = purchases
        context["purchases_cnt"] = (
            Purchase.objects.using("java_wallet").filter(goods_id=obj.id).count()
        )

        return context
