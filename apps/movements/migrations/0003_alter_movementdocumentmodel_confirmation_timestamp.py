# Generated by Django 4.0.5 on 2022-06-09 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movements', '0002_remove_movementdocumentmodel_receiver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movementdocumentmodel',
            name='confirmation_timestamp',
            field=models.DateTimeField(),
        ),
    ]