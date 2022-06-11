from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
import os

from .models import OrderDocumentModel, TMVOrderDocumentModel
from .serializers import ShortOrderDocumentSerializer, FullOrderDocumentSerializer, TMVOrderDocumentSerializer, \
    ShortOrderDocumentSerializer
from ..tmvs.serializers import TMVWarehouseSerializer
from ..procurements.serializers import ShortProcurementDocumentSerializer
from ..counterparties.models import CounterpartyModel
from ..counterparties.serializers import ShortCounterpartySerializer
from ..warehouses.models import WarehouseModel
from ..warehouses.serializers import ShortWarehouseSerializer

NOTIFICATION_SERVICE = os.environ.get('NOTIFICATION_SERVICE_URL')


class OrderDocumentListCreateView(ListCreateAPIView):
    queryset = OrderDocumentModel.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = FullOrderDocumentSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = ShortOrderDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        provider_id = serializer.data['provider']
        provider_data = ShortCounterpartySerializer(get_object_or_404(CounterpartyModel, id=provider_id)).data
        warehouse_id = serializer.data['warehouse']
        warehouse_data = ShortWarehouseSerializer(get_object_or_404(WarehouseModel, id=warehouse_id)).data

        data = {
            "receiver": provider_data['contact_data'],
            "message_text": f"На вас створено документ Замовлення ТМЦ №{serializer.data['id']} на склад "
                            f"{warehouse_data['name']} ({serializer.data['comment']})"

        }

        response = requests.post(NOTIFICATION_SERVICE, data=json.dumps(data), headers={
            'Content-type': 'application/json'
        })
        if int(response.status_code) != 200:
            return Response({'detail': 'Problem with notification'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDocumentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = FullOrderDocumentSerializer
    queryset = OrderDocumentModel.objects.all()

    def patch(self, request, *args, **kwargs):
        self.serializer_class = ShortOrderDocumentSerializer
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        lookup_fields = {
            'id': self.kwargs.get('order_id')
        }
        return get_object_or_404(self.queryset, **lookup_fields)

    def update(self, request, *args, **kwargs):
        if 'confirmation_status' in request.data and request.data['confirmation_status']:
            order_id = kwargs.get('order_id')

            order_instance = get_object_or_404(OrderDocumentModel, id=order_id)
            order_serializer = FullOrderDocumentSerializer(order_instance, {"confirmation_status": True}, partial=True)
            order_serializer.is_valid(raise_exception=True)
            order_serializer.save()
            order_data = order_serializer.data

            procurement_document_data = {
                "creator": order_data['provider']['id'],
                "confirmation_timestamp": order_data['confirmation_timestamp'],
                "comment": f'На основі Замовлення ТМЦ №{order_id}'
            }

            procurement_serializer = ShortProcurementDocumentSerializer(data=procurement_document_data)
            procurement_serializer.is_valid(raise_exception=True)
            procurement_serializer.save()

            order_items = TMVOrderDocumentModel.objects.filter(order_id=order_id)
            procurement_items = list()
            for order_item in order_items:
                procurement_items.append({
                    'number': order_item.actual_number,
                    'cost_per_unit': order_item.cost_per_unit,
                    'warehouse': order_data['warehouse']['id'],
                    'tmv': order_item.tmv.id,
                    'procurement_document': procurement_serializer.data['id'],
                    'date': procurement_serializer.data['confirmation_timestamp'].split('T')[0]
                })

            serializer = TMVWarehouseSerializer(data=procurement_items, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = {
                "receiver": order_data['creator']['contact_data'],
                "message_text": f"Ваше Замовлення ТМЦ №{order_data['id']} на склад "
                                f"{order_data['warehouse']['name']} ({order_data['comment']}) проведено"

            }

            response = requests.post(NOTIFICATION_SERVICE, data=json.dumps(data), headers={
                'Content-type': 'application/json'
            })
            if int(response.status_code) != 200:
                return Response({'detail': 'Problem with notification'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(order_serializer.data, status=status.HTTP_200_OK)

        return super().update(request, *args, **kwargs)


class OrderDocumentItemView(GenericAPIView):
    serializer_class = TMVOrderDocumentSerializer
    queryset = TMVOrderDocumentModel.objects.all()

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs.get('order_id')
        items = request.data['order_document_items']
        for item in items:
            item['order'] = order_id
            item_status = item.pop('status')
            try:
                if item_status == 'added':
                    serializer = TMVOrderDocumentSerializer(data=item)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                elif item_status == 'updated':
                    item_instance = get_object_or_404(TMVOrderDocumentModel.objects.all(), id=item['id'])
                    serializer = TMVOrderDocumentSerializer(item_instance, data=item, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                elif item_status == 'deleted':
                    item_instance = get_object_or_404(TMVOrderDocumentModel.objects.all(), id=item['id'])
                    item_instance.delete()

            except BaseException as error:
                return Response(f'Error {error}', status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)
