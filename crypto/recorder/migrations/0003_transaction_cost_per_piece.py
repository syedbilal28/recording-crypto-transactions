# Generated by Django 3.2.4 on 2021-07-11 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recorder', '0002_alter_transaction_profit'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='cost_per_piece',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]