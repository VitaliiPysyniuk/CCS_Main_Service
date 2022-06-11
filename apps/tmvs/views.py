from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404

from .models import TMVModel, TMVTypeModel, TMVUnitModel, TMVWarehouseModel
from .serializers import FullTMVSerializer, ShortTMVSerializer, TMVTypeSerializer, TMVUnitSerializer, \
    TMVWarehouseSerializer


class TMVTypeListCreateView(ListCreateAPIView):
    serializer_class = TMVTypeSerializer
    queryset = TMVTypeModel.objects.all()


class TMVTypeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TMVTypeSerializer
    queryset = TMVTypeModel.objects.all()

    def get_object(self):
        lookup_fields = {
            'id': self.kwargs.get('type_id')
        }
        return get_object_or_404(self.queryset, **lookup_fields)


class TMVUnitListCreateView(ListCreateAPIView):
    serializer_class = TMVUnitSerializer
    queryset = TMVUnitModel.objects.all()


class TMVUnitRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TMVUnitSerializer
    queryset = TMVUnitModel.objects.all()

    def get_object(self):
        lookup_fields = {
            'id': self.kwargs.get('unit_id')
        }
        return get_object_or_404(self.queryset, **lookup_fields)


class TMVListCreateView(ListCreateAPIView):
    queryset = TMVModel.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = FullTMVSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = ShortTMVSerializer
        return super().post(request, *args, **kwargs)


class TMVRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ShortTMVSerializer
    queryset = TMVModel.objects.all()

    def get_object(self):
        lookup_fields = {
            'id': self.kwargs.get('tmv_id')
        }
        return get_object_or_404(self.queryset, **lookup_fields)


class TMVWarehouseListCreateView(ListCreateAPIView):
    serializer_class = TMVWarehouseSerializer
    queryset = TMVWarehouseModel.objects.all()


class TMVWarehouseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = TMVWarehouseSerializer
    queryset = TMVWarehouseModel.objects.all()

    def get_object(self):
        lookup_fields = {
            'id': self.kwargs.get('item_id')
        }
        return get_object_or_404(self.queryset, **lookup_fields)
