# Generated by Django 4.0.4 on 2022-05-07 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('counterparties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WarehouseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('foreman', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='working_objects', to='counterparties.counterpartymodel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='own_objects', to='counterparties.counterpartymodel')),
            ],
            options={
                'db_table': 'warehouses',
            },
        ),
    ]