from rest_framework.serializers import ModelSerializer

from .models import TMVTypeModel, TMVUnitModel, TMVModel, TMVWarehouseModel
from ..warehouses.serializers import FullWarehouseSerializer


class TMVTypeSerializer(ModelSerializer):
    class Meta:
        model = TMVTypeModel
        fields = ['id', 'name']


class TMVUnitSerializer(ModelSerializer):
    class Meta:
        model = TMVUnitModel
        fields = ['id', 'name']


class ShortTMVSerializer(ModelSerializer):
    class Meta:
        model = TMVModel
        fields = ['id', 'name', 'unit', 'type']


class FullTMVSerializer(ModelSerializer):
    unit = TMVUnitSerializer(required=False)
    type = TMVTypeSerializer(required=False)

    class Meta:
        model = TMVModel
        fields = ['id', 'name', 'unit', 'type']


class TMVWarehouseSerializer(ModelSerializer):
    class Meta:
        model = TMVWarehouseModel
        fields = '__all__'
        extra_kwargs = {'procurement_document': {'required': False}, 'movement_document': {'required': False}}


class FullTMVWarehouseSerializer(ModelSerializer):
    tmv = FullTMVSerializer(required=False)
    warehouse = FullWarehouseSerializer(required=False)

    class Meta:
        model = TMVWarehouseModel
        fields = '__all__'
        extra_kwargs = {'procurement_document': {'required': False}, 'movement_document': {'required': False}}
