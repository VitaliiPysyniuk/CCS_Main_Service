from rest_framework.serializers import ModelSerializer

from .models import WarehouseModel
from ..counterparties.serializers import FullCounterpartySerializer
from ..tmvs.models import TMVWarehouseModel

class ShortWarehouseSerializer(ModelSerializer):
    class Meta:
        model = WarehouseModel
        fields = '__all__'


class FullWarehouseSerializer(ModelSerializer):
    owner = FullCounterpartySerializer(required=False)
    foreman = FullCounterpartySerializer(required=False)

    class Meta:
        model = WarehouseModel
        fields = '__all__'


class WarehouseRemnantSerializer(ModelSerializer):
    class Meta:
        model = TMVWarehouseModel
        fields = ['tmv']
        extra_fields = ['total_number', 'total_cost', 'cost_per_unit']
