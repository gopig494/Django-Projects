# Generated by Django 5.0.4 on 2024-04-16 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0094_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='price',
            field=models.DecimalField(decimal_places=2, default=20, max_digits=10),
            preserve_default=False,
        ),
    ]
