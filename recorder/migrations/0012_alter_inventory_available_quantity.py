# Generated by Django 3.2.4 on 2021-07-02 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recorder', '0011_auto_20210702_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='available_quantity',
            field=models.IntegerField(default=0),
        ),
    ]
