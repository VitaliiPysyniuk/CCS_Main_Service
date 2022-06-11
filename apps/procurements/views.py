from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import ProcurementDocumentModel
from .serializers import FullProcurementDocumentSerializer, ShortProcurementDocumentSerializer
from ..tmvs.serializers import TMVWarehouseSerializer
from ..tmvs.models import TMVWarehouseModel


class ProcurementDocumentListCreateView(ListCreateAPIView):
    queryset = ProcurementDocumentModel.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = FullProcurementDocumentSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = ShortProcurementDocumentSerializer
        return super().post(request, *args, **kwargs)


class ProcurementDocumentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = FullProcurementDocumentSerializer
    queryset = ProcurementDocumentModel.objects.all()

    def get_object(self):
        lookup_fields = {
            'id': self.kwargs.get('procurement_id')
        }
        return get_object_or_404(self.queryset, **lookup_fields)

    def update(self, request, *args, **kwargs):
        if 'confirmation_status' in request.data:
            procurement_id = kwargs.get('procurement_id')
            data = {'confirmation_status': request.data['confirmation_status']}
            procurement_items = TMVWarehouseModel.objects.filter(procurement_document_id=procurement_id)
            for procurement_item in procurement_items:
                serializer = TMVWarehouseSerializer(procurement_item, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return super().update(request, *args, **kwargs)


class ProcurementDocumentItemView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        procurement_id = self.kwargs.get('procurement_id')
        items = request.data['procurement_document_items']
        for item in items:
            item['procurement_document'] = procurement_id
            item_status = item.pop('status')
            try:
                if item_status == 'added':
                    serializer = TMVWarehouseSerializer(data=item)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                elif item_status == 'updated':
                    item_instance = get_object_or_404(TMVWarehouseModel.objects.all(), id=item['id'])
                    serializer = TMVWarehouseSerializer(item_instance, data=item, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                elif item_status == 'deleted':
                    item_instance = get_object_or_404(TMVWarehouseModel.objects.all(), id=item['id'])
                    item_instance.delete()

            except BaseException as error:
                return Response(f'Error {error}', status=status.HTTP_404_NOT_FOUND)

        return Response(data='Success', status=status.HTTP_200_OK)
