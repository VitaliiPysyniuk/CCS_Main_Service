# Generated by Django 4.0.4 on 2022-05-07 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('warehouses', '0001_initial'),
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdocumentmodel',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='warehouses.warehousemodel'),
        ),
    ]