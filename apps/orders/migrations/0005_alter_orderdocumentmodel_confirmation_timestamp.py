# Generated by Django 4.0.5 on 2022-06-10 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_tmvorderdocumentmodel_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdocumentmodel',
            name='confirmation_timestamp',
            field=models.DateTimeField(),
        ),
    ]
