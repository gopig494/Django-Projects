# Generated by Django 5.0.4 on 2024-05-08 03:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Learning_ORM_queries', '0008_alter_location_parent_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='parent_location',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Learning_ORM_queries.location'),
        ),
    ]
