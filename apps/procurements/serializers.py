from rest_framework.serializers import ModelSerializer

from .models import ProcurementDocumentModel
from ..tmvs.serializers import TMVWarehouseSerializer, FullTMVWarehouseSerializer
from ..counterparties.serializers import ShortCounterpartySerializer


class ShortProcurementDocumentSerializer(ModelSerializer):
    procurement_document_items = TMVWarehouseSerializer(many=True, required=False)

    class Meta:
        model = ProcurementDocumentModel
        fields = '__all__'
        extra_fields = ['procurement_document_items']


class FullProcurementDocumentSerializer(ModelSerializer):
    procurement_document_items = FullTMVWarehouseSerializer(many=True, required=False)
    creator = ShortCounterpartySerializer(required=False)

    class Meta:
        model = ProcurementDocumentModel
        fields = '__all__'
        extra_fields = ['procurement_document_items']
