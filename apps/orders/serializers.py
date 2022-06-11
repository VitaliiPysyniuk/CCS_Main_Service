from rest_framework.serializers import ModelSerializer

from .models import OrderDocumentModel, TMVOrderDocumentModel
from ..warehouses.serializers import ShortWarehouseSerializer
from ..counterparties.serializers import ShortCounterpartySerializer
from ..tmvs.serializers import FullTMVSerializer


class ShortOrderDocumentSerializer(ModelSerializer):
    class Meta:
        model = OrderDocumentModel
        fields = '__all__'


class TMVOrderDocumentSerializer(ModelSerializer):
    class Meta:
        model = TMVOrderDocumentModel
        fields = '__all__'


class FullTMVOrderDocumentSerializer(ModelSerializer):
    tmv = FullTMVSerializer(required=False)

    class Meta:
        model = TMVOrderDocumentModel
        fields = '__all__'


class FullOrderDocumentSerializer(ModelSerializer):
    order_document_items = FullTMVOrderDocumentSerializer(many=True, required=False)
    creator = ShortCounterpartySerializer(required=False)
    provider = ShortCounterpartySerializer(required=False)
    warehouse = ShortWarehouseSerializer(required=False)

    class Meta:
        model = OrderDocumentModel
        fields = '__all__'


class ShortOrderDocumentSerializer(ModelSerializer):
    order_document_items = FullTMVOrderDocumentSerializer(many=True, required=False)

    class Meta:
        model = OrderDocumentModel
        fields = '__all__'
