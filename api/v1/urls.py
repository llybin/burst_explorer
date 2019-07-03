from rest_framework import routers

from api.v1 import views

router = routers.DefaultRouter()

router.register('pending_txs', views.PendingTxsList, basename='pending_txs')

urlpatterns = router.urls
