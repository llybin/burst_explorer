from datetime import datetime

from rest_framework import serializers

from java_wallet.constants import BLOCK_CHAIN_START_AT, TxSubtypePayment


class PendingTxsSerializer(serializers.Serializer):
    type = serializers.IntegerField(read_only=True)
    subtype = serializers.IntegerField(read_only=True)
    timestamp = serializers.SerializerMethodField(read_only=True)
    amountNQT = serializers.IntegerField(read_only=True)
    feeNQT = serializers.IntegerField(read_only=True)
    sender = serializers.IntegerField(read_only=True)
    recipient = serializers.IntegerField(read_only=True)
    recipients = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_timestamp(data):
        return datetime.fromtimestamp(data['timestamp'] + BLOCK_CHAIN_START_AT)

    def get_recipients(self, data):
        result = []

        if data['subtype'] == TxSubtypePayment.MULTI_OUT:
            for x in data['attachment']['recipients']:
                result.append({'address': int(x[0]), 'amount': int(x[1])})

        elif data['subtype'] == TxSubtypePayment.MULTI_OUT_SAME:
            amount = int(data['amountNQT']) / len(data['attachment']['recipients'])
            for x in data['attachment']['recipients']:
                result.append({'address': int(x), 'amount': amount})

        return result or None

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
