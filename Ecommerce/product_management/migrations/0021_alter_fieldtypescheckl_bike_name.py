# Generated by Django 4.2.5 on 2024-04-11 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0020_alter_fieldtypescheckl_bike_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldtypescheckl',
            name='bike_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
