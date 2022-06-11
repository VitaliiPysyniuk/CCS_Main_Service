from django.db import models
from django.core.validators import MinLengthValidator


class CounterpartyTypeModel(models.Model):
    class Meta:
        db_table = 'counterparty_types'

    name = models.CharField(max_length=32, unique=True)


class CounterpartyModel(models.Model):
    class Meta:
        db_table = 'counterparties'

    name = models.CharField(max_length=64, unique=True)
    contact_data = models.CharField(max_length=13, unique=True, validators=[MinLengthValidator(13)])

    type = models.ForeignKey(CounterpartyTypeModel, on_delete=models.PROTECT, related_name='counterparties')
