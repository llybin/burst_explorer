from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from sentry_sdk import capture_exception

from api.v1.serializers import PendingTxsSerializer
from burst.api.brs.v1.api import BrsApi
from burst.api.exceptions import APIException


class PendingTxsList(ViewSet):
    @staticmethod
    def list(request):
        try:
            txs = BrsApi(settings.BRS_NODE).get_unconfirmed_transactions()
            txs.sort(key=lambda _x: int(_x["feeNQT"]), reverse=True)

            serializer = PendingTxsSerializer(txs, many=True)
            result = serializer.data
        except (APIException, ValueError) as e:
            capture_exception(e)
            result = []

        return Response(result)
