# Generated by Django 3.2.8 on 2021-11-06 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0008_auto_20211104_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='number',
            field=models.PositiveIntegerField(),
        ),
    ]
