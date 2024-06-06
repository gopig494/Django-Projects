# Generated by Django 5.0.4 on 2024-05-08 03:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0011_car'),
        ('product_management', '0098_rename_model_no_car_model_nos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_management.category', verbose_name='Category Name')),
            ],
        ),
    ]