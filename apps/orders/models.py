from django.db import models
from ..counterparties.models import CounterpartyModel
from ..warehouses.models import WarehouseModel
from ..tmvs.models import TMVModel
from decimal import Decimal


class OrderDocumentModel(models.Model):
    class Meta:
        db_table = 'order_documents'

    confirmation_status = models.BooleanField(default=False)
    confirmation_timestamp = models.DateTimeField()
    comment = models.CharField(max_length=128, blank=True)

    creator = models.ForeignKey(CounterpartyModel, on_delete=models.PROTECT, related_name='created_orders')
    provider = models.ForeignKey(CounterpartyModel, on_delete=models.PROTECT, related_name='provided_orders')
    warehouse = models.ForeignKey(WarehouseModel, on_delete=models.PROTECT, related_name='orders')


class TMVOrderDocumentModel(models.Model):
    class Meta:
        db_table = 'tmvs_orders'

    ordered_number = models.FloatField()
    actual_number = models.FloatField(default=0.0)
    cost_per_unit = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0000.00'))
    comment = models.CharField(max_length=128, blank=True)

    order = models.ForeignKey(OrderDocumentModel, on_delete=models.CASCADE, related_name='order_document_items')
    tmv = models.ForeignKey(TMVModel, on_delete=models.PROTECT, related_name='related_orders')
