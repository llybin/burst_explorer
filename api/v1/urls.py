from rest_framework import routers

from api.v1.views import PendingTxsList

router = routers.DefaultRouter()

router.register("pending_txs", PendingTxsList, basename="pending-txs-list")

urlpatterns = router.urls
