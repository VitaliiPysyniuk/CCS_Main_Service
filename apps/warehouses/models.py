from django.db import models
from ..counterparties.models import CounterpartyModel


class WarehouseModel(models.Model):
    class Meta:
        db_table = 'warehouses'

    name = models.CharField(max_length=64, unique=True)

    owner = models.ForeignKey(CounterpartyModel, on_delete=models.PROTECT, related_name='own_objects')
    foreman = models.ForeignKey(CounterpartyModel, on_delete=models.PROTECT, related_name='working_objects')
