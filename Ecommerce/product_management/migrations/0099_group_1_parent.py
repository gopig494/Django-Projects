# Generated by Django 5.0.4 on 2024-05-09 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0098_rename_model_no_car_model_nos'),
    ]

    operations = [
        migrations.AddField(
            model_name='group_1',
            name='parent',
            field=models.ManyToManyField(to='product_management.parent'),
        ),
    ]
