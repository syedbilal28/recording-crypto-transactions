# Generated by Django 3.2.4 on 2021-06-14 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recorder', '0003_transaction_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateField(),
        ),
    ]
