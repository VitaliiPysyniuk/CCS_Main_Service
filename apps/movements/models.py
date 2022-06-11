from django.db import models
from ..counterparties.models import CounterpartyModel
from ..warehouses.models import WarehouseModel


class MovementDocumentModel(models.Model):
    class Meta:
        db_table = 'movement_documents'

    confirmation_status = models.BooleanField(default=False)
    confirmation_timestamp = models.DateTimeField()
    comment = models.CharField(max_length=128, blank=True)

    creator = models.ForeignKey(CounterpartyModel, on_delete=models.PROTECT, related_name='created_movements')
    from_warehouse = models.ForeignKey(WarehouseModel, on_delete=models.PROTECT, related_name='sent_movements')
    to_warehouse = models.ForeignKey(WarehouseModel, on_delete=models.PROTECT, related_name='received_movements')
