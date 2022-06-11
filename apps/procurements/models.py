from django.db import models
from ..counterparties.models import CounterpartyModel


class ProcurementDocumentModel(models.Model):
    class Meta:
        db_table = 'procurement_documents'

    confirmation_status = models.BooleanField(default=False)
    confirmation_timestamp = models.DateTimeField()
    comment = models.CharField(max_length=128, blank=True)

    creator = models.ForeignKey(CounterpartyModel, on_delete=models.PROTECT, related_name='procurement_documents')
