# Generated by Django 3.2.4 on 2021-06-14 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recorder', '0005_remove_transaction_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='percentage',
            field=models.FloatField(blank=True, null=True),
        ),
    ]