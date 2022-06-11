from rest_framework.serializers import ModelSerializer

from .models import MovementDocumentModel
from ..tmvs.serializers import TMVWarehouseSerializer, FullTMVWarehouseSerializer
from ..warehouses.serializers import ShortWarehouseSerializer
from ..counterparties.serializers import ShortCounterpartySerializer


class ShortMovementDocumentSerializer(ModelSerializer):
    movement_document_items = TMVWarehouseSerializer(many=True, required=False)

    class Meta:
        model = MovementDocumentModel
        fields = '__all__'
        extra_fields = ['movement_document_items']


class FullMovementDocumentSerializer(ModelSerializer):
    movement_document_items = FullTMVWarehouseSerializer(many=True, required=False)
    creator = ShortCounterpartySerializer(required=False)
    from_warehouse = ShortWarehouseSerializer(required=False)
    to_warehouse = ShortWarehouseSerializer(required=False)

    class Meta:
        model = MovementDocumentModel
        fields = '__all__'
        extra_fields = ['movement_document_items']
