# Generated by Django 4.0.4 on 2022-05-12 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tmvorderdocumentmodel',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_document_items', to='orders.orderdocumentmodel'),
        ),
    ]
