from rest_framework.serializers import ModelSerializer

from .models import CounterpartyModel, CounterpartyTypeModel


class CounterpartyTypeSerializer(ModelSerializer):
    class Meta:
        model = CounterpartyTypeModel
        fields = ['id', 'name']


class FullCounterpartySerializer(ModelSerializer):
    type = CounterpartyTypeSerializer(required=True)

    class Meta:
        model = CounterpartyModel
        fields = ['id', 'name', 'type', 'contact_data']


class ShortCounterpartySerializer(ModelSerializer):

    class Meta:
        model = CounterpartyModel
        fields = ['id', 'name', 'type', 'contact_data']
