from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F, FloatField

from .models import WarehouseModel
from .serializers import ShortWarehouseSerializer, FullWarehouseSerializer
from ..tmvs.models import TMVWarehouseModel, TMVModel
from ..tmvs.serializers import ShortTMVSerializer, FullTMVWarehouseSerializer, FullTMVSerializer


class WarehouseListCreateView(ListCreateAPIView):
    queryset = WarehouseModel.objects.all()

    def get(self, request, *args, **kwargs):
        self.serializer_class = FullWarehouseSerializer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = ShortWarehouseSerializer
        return super().post(request, *args, **kwargs)


class WarehouseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = ShortWarehouseSerializer
    queryset = WarehouseModel.objects.all()

    def get_object(self):
        lookup_fields = {
            'id': self.kwargs.get('warehouse_id')
        }
        return get_object_or_404(self.queryset, **lookup_fields)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        warehouse_data = FullWarehouseSerializer(instance).data
        item_instances = TMVWarehouseModel.objects.filter(warehouse=warehouse_data['id'], confirmation_status=True)
        result = item_instances.values('tmv'). \
            annotate(total_number=Sum('number'),
                     cost_per_unit=((Sum(F('number') * F('cost_per_unit'), output_field=FloatField())) / Sum('number')))

        for i in range(len(result)):
            tmv_id = result[i]['tmv']
            tmv_instance = TMVModel.objects.filter(id=tmv_id)[0]
            tmv_data = ShortTMVSerializer(instance=tmv_instance).data
            result[i]['tmv'] = tmv_data
        warehouse_data['tmvs'] = result

        return Response(warehouse_data, status=status.HTTP_200_OK)


class WarehouseItemView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        warehouse_id = kwargs.get('warehouse_id')
        tmv_id = kwargs.get('tmv_id')
        item_instances = TMVWarehouseModel.objects.filter(warehouse=warehouse_id, tmv=tmv_id,
                                                          confirmation_status=True)
        print(item_instances)
        result = item_instances.values('tmv'). \
            annotate(total_number=Sum('number'),
                     cost_per_unit=((Sum(F('number') * F('cost_per_unit'), output_field=FloatField())) / Sum('number')))

        return Response(result, status=status.HTTP_200_OK)


class WarehouseItemsView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        warehouse_id = kwargs.get('warehouse_id')
        query_params = self.request.query_params
        result = TMVWarehouseModel.objects.filter(warehouse=warehouse_id, confirmation_status=True)

        if 'date_from' in query_params:
            result = result.filter(date__gte=query_params['date_from'])

        if 'date_to' in query_params:
            result = result.filter(date__lte=query_params['date_to'])

        if 'tmv' in query_params:
            result = result.filter(tmv_id=query_params['tmv'])

        if 'tmv_type' in query_params:
            result = result.filter(tmv__type_id=query_params['tmv_type'])

        result = result.values('tmv').annotate(
            total_number=Sum('number'),
            total_cost=Sum(F('number') * F('cost_per_unit'), output_field=FloatField()))

        parsed_result = []
        for item in result:
            if item['total_number'] != 0:
                tmv_data = FullTMVSerializer(get_object_or_404(TMVModel, id=item['tmv'])).data
                item['tmv'] = tmv_data
                cost_per_unit = item['total_cost'] / item['total_number']
                item['cost_per_unit'] = cost_per_unit
                parsed_result.append(item)

        return Response({'tmvs': parsed_result}, status=status.HTTP_200_OK)


class WarehouseTMVTurnoverView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        query_params = self.request.query_params
        warehouse_id = kwargs.get('warehouse_id')

        result = TMVWarehouseModel.objects.filter(warehouse=warehouse_id, confirmation_status=True)

        if 'date_from' in query_params:
            result = result.filter(date__gte=query_params['date_from'])

        if 'date_to' in query_params:
            result = result.filter(date__lte=query_params['date_to'])

        if 'tmv' in query_params:
            result = result.filter(tmv_id=query_params['tmv'])

        if 'tmv_type' in query_params:
            result = result.filter(tmv__type_id=query_params['tmv_type'])

        data = FullTMVWarehouseSerializer(result, many=True).data

        parsed_data = {}
        for item in data:
            tmv = item.pop('tmv')
            item.pop('warehouse')
            if str(tmv['id']) in parsed_data:
                parsed_data[str(tmv['id'])]['actions'].append(item)
            else:
                parsed_data[str(tmv['id'])] = {}
                parsed_data[str(tmv['id'])]['tmv'] = tmv
                parsed_data[str(tmv['id'])]['actions'] = [item]

        return Response({'tmvs': parsed_data}, status=status.HTTP_200_OK)
