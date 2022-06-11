# Generated by Django 4.0.4 on 2022-05-10 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('procurements', '0001_initial'),
        ('movements', '0001_initial'),
        ('tmvs', '0004_alter_tmvwarehousemodel_movement_document_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmvwarehousemodel',
            name='movement_document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='movement_document_items', to='movements.movementdocumentmodel'),
        ),
        migrations.AlterField(
            model_name='tmvwarehousemodel',
            name='procurement_document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='procurement_document_items', to='procurements.procurementdocumentmodel'),
        ),
    ]
