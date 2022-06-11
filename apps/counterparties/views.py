from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.response import Response

from .models import CounterpartyModel, CounterpartyTypeModel
from .serializers import CounterpartyTypeSerializer, FullCounterpartySerializer, ShortCounterpartySerializer


class CounterpartyTypeListCreateView(ListCreateAPIView):
    queryset = CounterpartyTypeModel.objects.all()
    serializer_class = CounterpartyTypeSerializer


class CounterpartyTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CounterpartyTypeSerializer
    queryset = CounterpartyTypeModel.objects.all()

    def get_object(self):
        lookup_fields = {
            'id': self.kwargs.get('type_id')
        }
        return get_object_or_404(self.queryset, **lookup_fields)


class CounterpartyListCreateView(ListCreateAPIView):
    queryset = CounterpartyModel.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = FullCounterpartySerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = ShortCounterpartySerializer
        return super().post(request, *args, **kwargs)


class CounterpartyRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ShortCounterpartySerializer
    queryset = CounterpartyModel.objects.all()

    def get_object(self):
        lookup_fields = {
            'id': self.kwargs.get('counterparty_id')
        }
        return get_object_or_404(self.queryset, **lookup_fields)


class CounterpartyFilterRetrieveView(RetrieveAPIView):
    queryset = CounterpartyModel.objects.all()
    serializer_class = ShortCounterpartySerializer

    def get_object(self):
        query_params = self.request.query_params
        contact_data = f"+{query_params['contact_data']}".replace(' ', '')
        counterparty = get_object_or_404(CounterpartyModel, contact_data=contact_data)
        return counterparty
