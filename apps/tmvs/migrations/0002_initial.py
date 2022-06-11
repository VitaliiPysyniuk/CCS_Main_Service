# Generated by Django 4.0.4 on 2022-05-07 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('warehouses', '0001_initial'),
        ('tmvs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tmvwarehousemodel',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tmvs', to='warehouses.warehousemodel'),
        ),
        migrations.AddField(
            model_name='tmvmodel',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tmvs_types', to='tmvs.tmvtypemodel'),
        ),
        migrations.AddField(
            model_name='tmvmodel',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tmvs_units', to='tmvs.tmvunitmodel'),
        ),
    ]
