from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from copy import deepcopy
import requests
import os
import json

from .models import MovementDocumentModel
from .serializers import ShortMovementDocumentSerializer, FullMovementDocumentSerializer
from ..tmvs.models import TMVWarehouseModel
from ..tmvs.serializers import TMVWarehouseSerializer
from ..warehouses.models import WarehouseModel
from ..warehouses.serializers import ShortWarehouseSerializer, FullWarehouseSerializer
from ..counterparties.models import CounterpartyModel
from ..counterparties.serializers import ShortCounterpartySerializer

NOTIFICATION_SERVICE = os.environ.get('NOTIFICATION_SERVICE_URL')


class MovementDocumentListCreateView(ListCreateAPIView):
    serializer_class = ShortMovementDocumentSerializer
    queryset = MovementDocumentModel.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = FullMovementDocumentSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = ShortMovementDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        counterparty = ShortCounterpartySerializer(
            get_object_or_404(CounterpartyModel, id=serializer.data['creator'])).data
        warehouse = FullWarehouseSerializer(
            get_object_or_404(WarehouseModel, id=serializer.data['to_warehouse'])).data

        data = {
            "receiver": warehouse['foreman']['contact_data'],
            "message_text": f"На склад {warehouse['name']} створено переміщення "
                            f"№{serializer.data['id']} ({serializer.data['comment']})"
        }


        print(NOTIFICATION_SERVICE)
        print(data)

        response = requests.post(NOTIFICATION_SERVICE, data=json.dumps(data), headers={
            'Content-type': 'application/json'
        })
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovementDocumentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ShortMovementDocumentSerializer
    queryset = MovementDocumentModel.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = FullMovementDocumentSerializer
        return super().get(request, *args, **kwargs)

    def get_object(self):
        lookup_fields = {
            'id': self.kwargs.get('movement_id')
        }
        return get_object_or_404(self.queryset, **lookup_fields)

    def update(self, request, *args, **kwargs):
        if 'confirmation_status' in request.data:
            movement_id = kwargs.get('movement_id')
            data = {'confirmation_status': request.data['confirmation_status']}
            movement_items = TMVWarehouseModel.objects.filter(movement_document_id=movement_id)
            for movement_item in movement_items:
                serializer = TMVWarehouseSerializer(movement_item, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return super().update(request, *args, **kwargs)


class MovementDocumentItemView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        movement_id = kwargs.get('movement_id')
        from_warehouse = request.data['from_warehouse']
        to_warehouse = request.data['to_warehouse']
        items = request.data['movement_document_items']

        for item in items:
            item_status = item.pop('status')
            try:
                if item_status == 'added':
                    item['movement_document'] = movement_id
                    item_1 = deepcopy(item)
                    item_1['warehouse'] = to_warehouse
                    item_2 = deepcopy(item)
                    item_2['warehouse'] = from_warehouse
                    item_2['number'] = -item_1['number']
                    serializer = TMVWarehouseSerializer(data=[item_1, item_2], many=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                elif item_status == 'updated':
                    # item_instances = TMVWarehouseModel.objects.filter(movement_document=movement_id, tmv=item['tmv'])
                    # for instance in item_instances:
                    #     new_item = deepcopy(item)
                    #     instance_data = TMVWarehouseSerializer(instance).data
                    #     if instance_data['number'] < 0:
                    #         new_item['number'] = -item['number']
                    #     serializer = TMVWarehouseSerializer(instance, data=new_item, partial=True)
                    #     serializer.is_valid(raise_exception=True)
                    #     serializer.save()

                    # item_instance = TMVWarehouseModel.objects.filter(movement_document=movement_id, id=item.id).first()
                    item_instance = get_object_or_404(TMVWarehouseModel, id=item['id'])
                    new_item = deepcopy(item)
                    instance_data = TMVWarehouseSerializer(item_instance).data
                    # if instance_data['number'] < 0:
                    #     new_item['number'] = -item['number']
                    serializer = TMVWarehouseSerializer(item_instance, data=new_item, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                elif item_status == 'deleted':
                    # item_instances = TMVWarehouseModel.objects.filter(movement_document=movement_id, tmv=item['tmv'])
                    # for instance in item_instances:
                    #     instance.delete()

                    item_instance = get_object_or_404(TMVWarehouseModel, id=item['id'])
                    item_instance.delete()

            except BaseException as error:
                return Response(f'Error {error}', status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)
