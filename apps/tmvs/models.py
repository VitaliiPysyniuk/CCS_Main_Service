from django.db import models
from ..warehouses.models import WarehouseModel
from ..procurements.models import ProcurementDocumentModel
from ..movements.models import MovementDocumentModel
from decimal import Decimal


class TMVTypeModel(models.Model):
    class Meta:
        db_table = 'tmv_types'

    name = models.CharField(max_length=32, unique=True)


class TMVUnitModel(models.Model):
    class Meta:
        db_table = 'units'

    name = models.CharField(max_length=8, unique=True)


class TMVModel(models.Model):
    class Meta:
        db_table = 'tmvs'

    name = models.CharField(max_length=128, unique=True)

    type = models.ForeignKey(TMVTypeModel, on_delete=models.PROTECT, related_name='tmvs_types')
    unit = models.ForeignKey(TMVUnitModel, on_delete=models.PROTECT, related_name='tmvs_units')


class TMVWarehouseModel(models.Model):
    class Meta:
        db_table = 'tmvs_warehouses'

    number = models.FloatField(default=0.0)
    cost_per_unit = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0000.00'))
    date = models.DateField()
    confirmation_status = models.BooleanField(default=False)
    comment = models.CharField(max_length=128, blank=True)

    warehouse = models.ForeignKey(WarehouseModel, on_delete=models.PROTECT, related_name='tmvs')
    tmv = models.ForeignKey(TMVModel, on_delete=models.PROTECT, related_name='orders')
    procurement_document = models.ForeignKey(ProcurementDocumentModel, on_delete=models.CASCADE,
                                             related_name='procurement_document_items', null=True)
    movement_document = models.ForeignKey(MovementDocumentModel, on_delete=models.CASCADE,
                                          related_name='movement_document_items', null=True)
